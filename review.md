# Creamy Delights (SriProject) — Full Project Review & Deployment Guide

> **Status:** 🟢 Deployment-Ready  
> **Target Platform:** Railway (Single Unified Web Service + PostgreSQL + Persistent Volume)  
> **Production Custom Domain:** `creamydelights.in` (and `www.creamydelights.in`)  
> **Railway Service Hostname:** e.g., `creamy-delights-production.up.railway.app`

---

## 1. Routing Verification & Typo Resolution

### Verification Result: Code is 100% Correct
The question raised regarding the architecture diagram label on page 19 (`/media/*` serving Astro `dist/`) was an **editorial documentation typo only**. 

In the actual code implementation located at [`backend/config/urls.py`](file:///Users/antojero/Documents/SriProject/backend/config/urls.py), the routing order and destinations are strictly verified:

```python
urlpatterns = [
    # 1. Django Admin
    path("admin/", admin.site.urls),

    # 2. Health Check Probe (Railway Liveness/Readiness)
    path("health/", health_check, name="health-check"),

    # 3. REST API endpoints
    path("", include("cakes.urls")),
    path("", include("gallery.urls")),
    path("", include("enquiries.urls")),   # POST /api/enquiries/

    # 4. Media Uploads (Django serve -> Volume /data/media/)
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),

    # 5. Astro Frontend Catch-all (Serves prebuilt HTML/CSS/JS from Astro dist/)
    re_path(r"^(?P<path>.*)$", serve_astro_frontend),
]
```

### Routing Resolution Summary
| URL Pattern | Handled By | Physical Path / Target | Description |
| :--- | :--- | :--- | :--- |
| `/admin/*` | Django `admin.site.urls` | Django Admin View | Superuser database management |
| `/health/` | `health_check()` view | Inline JSON `{"status": "ok"}` | Railway HTTP healthcheck (HTTP 200) |
| `/api/cakes/*` | `cakes.urls` | PostgreSQL Database | Cake catalogue, categories, pricing |
| `/api/gallery/*` | `gallery.urls` | PostgreSQL Database | Showcase images & videos |
| `/api/enquiries/*` | `enquiries.urls` | PostgreSQL Database | Contact submissions & WhatsApp flow |
| `/static/*` | WhiteNoise middleware | `backend/staticfiles/` | Admin CSS, JS, fonts |
| **`/media/*`** | **Django `serve()`** | **`/data/media/` (Railway Volume)** | **Customer & admin uploaded media** |
| **`/*`** | **`serve_astro_frontend()`** | **`dist/` (Astro static output)** | **Public website pages (`/`, `/about`, `/cakes`, etc.)** |

No architectural or codebase changes are required for routing.

---

## 2. ALLOWED_HOSTS & CSRF Configuration Review

### Why `*.up.railway.app` Should Not Be Used
1. **Django Wildcard Syntax:** In Django, wildcard subdomain matching uses a **leading dot** (e.g., `.up.railway.app`), NOT an asterisk (`*.up.railway.app`). Asterisks are not parsed by Django's `ALLOWED_HOSTS` validator.
2. **Production Best Practice:** In production, you should use the **exact Railway hostname** assigned to your Web Service once provisioned (e.g. `creamy-delights-production.up.railway.app`), along with your custom domains (`creamydelights.in`, `www.creamydelights.in`).
3. **Local Dev Isolation:** Local addresses (`localhost`, `127.0.0.1`) are kept for local development. In production (`DEBUG=False`), only production hostnames are allowed.

### Recommended Production Variable Values:
```ini
ALLOWED_HOSTS=creamy-delights-production.up.railway.app,creamydelights.in,www.creamydelights.in
CSRF_TRUSTED_ORIGINS=https://creamy-delights-production.up.railway.app,https://creamydelights.in,https://www.creamydelights.in
```
*(Replace `creamy-delights-production.up.railway.app` with the actual Railway public domain generated when creating the service).*

---

## 3. Target Production Architecture

The application runs as a **single unified Railway Web Service**, eliminating unnecessary multi-service billing and CORS complexities:

```
                            INTERNET / USERS
                                   │
                                   ▼
          HTTPS: creamydelights.in / Railway Hostname
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │    Railway Single Web Service    │
                  │   (Gunicorn on 0.0.0.0:$PORT)   │
                  └──────────────┬──────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   Astro Pages            Django REST API           Django Admin
  (Astro dist/)          (/api/cakes, etc.)          (/admin/)
   • /                     • /api/cakes/              • Superuser auth
   • /about                • /api/gallery/            • Product catalogue
   • /cakes                • /api/enquiries/          • Order tracking
   • /gallery              • /health/                 • Media moderation
   • /contact                    │
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
  Railway PostgreSQL      Railway Volume
   (${DATABASE_URL})       (Mount: /data)
   • Relational data       • /data/media/cakes/
   • Categories & Cakes    • /data/media/gallery/
   • Enquiries & Logs      • /data/media/gallery/thumbnails/
```

---

## 4. Current State of the Project Folder

Every file in the repository has a single, well-defined purpose:

```
SriProject/
├── .env.example                     <- Reference template for all production environment variables
├── nixpacks.toml                    <- Dual-runtime build setup (Node.js 22 + Python 3.12)
├── railway.toml                     <- Railway deployment spec (preDeployCommand migrations + Gunicorn)
├── package.json                     <- Astro frontend dependencies and build scripts
├── package-lock.json                <- Deterministic Node package lockfile
├── astro.config.mjs                 <- Astro configuration (output: 'static')
├── tsconfig.json                    <- TypeScript configuration for Astro
├── src/                             <- Astro Frontend Source Code
│   ├── components/
│   │   ├── Navbar.astro             <- Responsive header with brand logo & navigation links
│   │   ├── Footer.astro             <- Footer with store info, Tirunelveli location, contact links
│   │   ├── CakeCard.astro           <- Product display card with pricing, image, order button
│   │   └── WhatsAppButton.astro     <- Floating WhatsApp quick-enquiry action button
│   ├── layouts/
│   │   └── Layout.astro             <- Base HTML shell with SEO meta tags, Google Fonts, global CSS
│   ├── pages/
│   │   ├── index.astro              <- Landing page with hero banner, featured cakes, customer reviews
│   │   ├── about.astro              <- Bakery story, quality ingredients, baking craftsmanship
│   │   ├── cakes.astro              <- Dynamic catalogue consuming GET /api/cakes/
│   │   ├── gallery.astro            <- Visual gallery consuming GET /api/gallery/ (images & videos)
│   │   └── contact.astro            <- Contact form submitting to POST /api/enquiries/ + WhatsApp flow
│   └── styles/
│       └── global.css               <- CSS variables, responsive typography, modern color palette
├── dist/                            <- Generated prebuilt static frontend (served by Django in production)
└── backend/                         <- Django 5 Backend
    ├── manage.py                    <- Django CLI management utility
    ├── requirements.txt             <- Production dependencies: Django 5, DRF, psycopg2, Gunicorn, WhiteNoise, Pillow
    ├── staticfiles/                 <- Production collected static assets from 'collectstatic'
    ├── config/
    │   ├── settings.py              <- Production settings: WhiteNoise, PostgreSQL db_url, auto-mkdir for media
    │   ├── urls.py                  <- Master routing: Admin -> Health -> APIs -> Media (/data/media) -> Astro dist/
    │   └── wsgi.py                  <- WSGI application callable for Gunicorn
    ├── cakes/                       <- Cake Catalogue App
    │   ├── models.py                <- Category, Cake, CakeVariant models
    │   ├── serializers.py           <- DRF serializers formatting full image URLs
    │   ├── views.py                 <- Read-only API endpoints for cakes and categories
    │   ├── urls.py                  <- Routes for /api/cakes/ and /api/categories/
    │   ├── admin.py                 <- Django Admin with thumbnail previews and variant inlines
    │   └── migrations/              <- Database schema migrations
    ├── gallery/                     <- Media Gallery App
    │   ├── models.py                <- MediaItem model supporting images and video uploads
    │   ├── serializers.py           <- DRF serializers for gallery items
    │   ├── views.py                 <- Read-only API endpoint for gallery media
    │   ├── urls.py                  <- Route for /api/gallery/
    │   ├── admin.py                 <- Django Admin with video playback and thumbnail previews
    │   └── migrations/              <- Database schema migrations
    └── enquiries/                   <- Customer Enquiries App
        ├── models.py                <- Enquiry model (customer name, phone, cake selection, notes, status)
        ├── serializers.py           <- DRF EnquirySerializer with phone and payload validation
        ├── views.py                 <- POST /api/enquiries/ endpoint with CSRF exemption for form submissions
        ├── urls.py                  <- Route for /api/enquiries/
        ├── admin.py                 <- Django Admin with status filters, date hierarchy, WhatsApp quick-links
        └── migrations/              <- Database schema migrations
```

---

## 5. Key Architectural Details Verified

### A. Database Migrations via `preDeployCommand`
* **Rule**: Django migrations (`python manage.py migrate`) **MUST NEVER** run in the build phase (`[phases.build]`).
* **Why**: Railway build containers do not have private network connectivity to internal services like PostgreSQL.
* **Solution**: Migrations are executed in [`railway.toml`](file:///Users/antojero/Documents/SriProject/railway.toml) via `preDeployCommand`:
  ```toml
  [deploy]
  preDeployCommand = "cd backend && /opt/venv/bin/python manage.py migrate --noinput"
  startCommand = "cd backend && /opt/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
  healthcheckPath = "/health/"
  healthcheckTimeout = 300
  restartPolicyType = "ON_FAILURE"
  ```

### B. Persistent Media Volume Mounting & Auto-Initialization
* Railway volumes are mounted to the running container at **start time**, not during image compilation or pre-deploy.
* The volume mount path in Railway dashboard must be `/data`.
* In [`backend/config/settings.py`](file:///Users/antojero/Documents/SriProject/backend/config/settings.py), the application automatically checks and creates the required directory tree on boot:
  ```python
  MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))
  MEDIA_URL = "/media/"

  for _subdir in ["cakes", "gallery", "gallery/thumbnails"]:
      (MEDIA_ROOT / _subdir).mkdir(parents=True, exist_ok=True)
  ```
* This guarantees that upload folders always exist even if a fresh volume is mounted.

### C. Build Pipeline via `nixpacks.toml`
The container is built with both Node.js (for Astro) and Python (for Django):
```toml
[phases.setup]
nixPkgs = ["python312", "nodejs_22", "gcc"]

[phases.install]
cmds = [
  "npm ci",
  "python3 -m venv /opt/venv",
  "/opt/venv/bin/pip install --upgrade pip",
  "/opt/venv/bin/pip install -r backend/requirements.txt"
]

[phases.build]
cmds = [
  "npm run build",
  "cd backend && /opt/venv/bin/python manage.py collectstatic --noinput"
]

[start]
cmd = "cd backend && /opt/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
```

---

## 6. Railway Configuration Variables

In your Web Service → **Variables** tab, set:

| Variable Name | Recommended Value | Description |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | *(Generate a 50-character random key)* | Secret key for Django cryptographic signing |
| `DEBUG` | `False` | Disables debug mode in production |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Railway reference linking the PostgreSQL database |
| `MEDIA_ROOT` | `/data/media` | Target folder inside the mounted Railway Volume |
| `ALLOWED_HOSTS` | `creamy-delights-production.up.railway.app,creamydelights.in,www.creamydelights.in` | Exact Railway hostname + custom domain |
| `CSRF_TRUSTED_ORIGINS` | `https://creamy-delights-production.up.railway.app,https://creamydelights.in,https://www.creamydelights.in` | Trusted origins for admin forms |
| `PYTHONUNBUFFERED` | `1` | Ensures real-time console log streaming |

> [!IMPORTANT]
> **Check 1: No Escaped Backslashes (`\`)**  
> Ensure strings pasted into Railway contain NO backslashes:
> * ✅ `www.creamydelights.in` (NOT `www\.creamydelights.in`)
> * ✅ `https://creamydelights.in` (NOT `https\://creamydelights.in`)
>
> **Check 2: Verify `DATABASE_URL` Service Name**  
> `${{Postgres.DATABASE_URL}}` works when the database service in your Railway project is named `Postgres`. If Railway names it `PostgreSQL` or `Database`, use Railway's variable selector (type `${{` to pick the reference variable directly) or copy the Postgres Connection URL.
>
> **Check 3: Mount Path Must Be `/data` Exactly**  
> The Volume mount path must be set to `/data` so that `MEDIA_ROOT=/data/media` automatically resolves to persistent disk storage.

---

## 7. Complete 15-Step Deployment Runbook

Follow this exact workflow from local workspace to full production launch:

1. **Push final code to GitHub**:
   ```bash
   git add -A
   git commit -m "chore: ready for railway deployment"
   git push origin main
   ```
2. **Create Railway Project**: Click **New Project** in Railway Dashboard.
3. **Deploy SriProject from GitHub**: Select your `SriProject` GitHub repository.
4. **Add PostgreSQL**: Click **+ New** → **Database** → **PostgreSQL**.
5. **Add Volume → `/data`**: On Web Service, go to **Volumes** → **Add Volume** with mount path `/data`.
6. **Add Environment Variables**: Populate `DJANGO_SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `MEDIA_ROOT=/data/media`, `PYTHONUNBUFFERED=1`.
7. **Generate Railway Domain**: Go to Web Service **Settings** → **Networking** → **Generate Domain** (e.g. `creamy-delights-production.up.railway.app`).
8. **Update `ALLOWED_HOSTS` & `CSRF_TRUSTED_ORIGINS`**: Paste your actual generated domain into Railway variables without backslashes.
9. **Deploy**: Railway runs `npm ci` → `npm run build` → `collectstatic` → pre-deploy `migrate` → starts `gunicorn`.
10. **Check `/health/`**: Visit `https://<your-domain>.up.railway.app/health/` and confirm `{"status": "ok"}`.
11. **Create Django Superuser**: Open Railway Web Terminal and run:
    ```bash
    /opt/venv/bin/python backend/manage.py createsuperuser
    ```
12. **Login to `/admin/`**: Open `https://<your-domain>.up.railway.app/admin/` and log in with your superuser credentials.
13. **Add Cakes & Gallery via Admin**: Upload sample cakes, categories, and gallery media to test volume persistence.
14. **Test Website**: Verify all 11 routes using the test matrix below.
15. **Connect `creamydelights.in`**: Add custom domain under **Settings** → **Networking** → **Custom Domain**, update DNS records, and let Railway provision the SSL certificate.

---

## 8. Post-Deploy URL Verification Matrix

Test each endpoint after deployment on your Railway URL (`https://<your-service>.up.railway.app`):

| Test Route | Expected Response / Behavior |
| :--- | :--- |
| `GET /` | Astro Landing page loads with CSS, images, and typography |
| `GET /about` | About page rendered cleanly |
| `GET /cakes` | Catalogue loads and renders products from `/api/cakes/` |
| `GET /gallery` | Gallery loads images & video cards from `/api/gallery/` |
| `GET /contact` | Contact form submits to `/api/enquiries/` + triggers WhatsApp |
| `GET /health/` | Returns `{"status": "ok"}` with HTTP 200 |
| `GET /api/cakes/` | Returns JSON array of cakes and categories |
| `GET /api/gallery/` | Returns JSON array of media items |
| `POST /api/enquiries/` | Accepts customer enquiry JSON payload, returns HTTP 201 |
| `GET /admin/` | Django Admin login screen renders with complete CSS |
| `GET /media/...` | Successfully serves uploaded image from `/data/media/...` |
