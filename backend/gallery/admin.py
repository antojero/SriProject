from django.contrib import admin
from .models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "category", "published", "created_at")
    list_filter = ("type", "category", "published")
    search_fields = ("title",)
