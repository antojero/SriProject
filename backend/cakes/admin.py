from django.contrib import admin
from .models import Cake

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("name", "featured", "published", "updated_at")
    list_filter = ("featured", "published")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
