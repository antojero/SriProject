import os
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse, Http404

DIST_DIR = settings.BASE_DIR.parent / "dist"

def serve_astro_frontend(request, path=""):
    clean_path = path.strip("/")
    if not clean_path:
        target_file = DIST_DIR / "index.html"
    else:
        target_file = DIST_DIR / clean_path
        if not target_file.exists() or target_file.is_dir():
            target_file = DIST_DIR / clean_path / "index.html"

    if target_file.exists() and target_file.is_file():
        content_type = "text/html"
        suffix = target_file.suffix.lower()
        if suffix == ".css":
            content_type = "text/css"
        elif suffix == ".js":
            content_type = "application/javascript"
        elif suffix in [".jpg", ".jpeg"]:
            content_type = "image/jpeg"
        elif suffix == ".webp":
            content_type = "image/webp"
        elif suffix == ".svg":
            content_type = "image/svg+xml"
        elif suffix == ".png":
            content_type = "image/png"
        elif suffix == ".mp4":
            content_type = "video/mp4"

        with open(target_file, "rb") as f:
            return HttpResponse(f.read(), content_type=content_type)

    raise Http404("Frontend page not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cakes.urls')),
    path('', include('gallery.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^(?P<path>.*)$', serve_astro_frontend),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
