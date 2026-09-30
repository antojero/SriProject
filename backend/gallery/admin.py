from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "category", "published", "created_at")
    list_filter = ("type", "category", "published")
    list_editable = ("published",)
    search_fields = ("title",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {
            "fields": ("title", "type", "category"),
        }),
        ("Media Content", {
            "description": "For images/videos upload a file. For Instagram Reels paste the URL below.",
            "fields": ("file", "thumbnail", "instagram_url"),
        }),
        ("Visibility", {
            "fields": ("published",),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
