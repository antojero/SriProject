from django.contrib import admin
from .models import Cake


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("name", "featured", "published", "created_at", "updated_at")
    list_filter = ("featured", "published")
    list_editable = ("featured", "published")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "description", "image"),
        }),
        ("Visibility", {
            "fields": ("published", "featured"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
