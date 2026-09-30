from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "cake_type", "required_date", "status", "created_at")
    list_filter = ("status", "required_date", "created_at")
    list_editable = ("status",)
    search_fields = ("name", "phone", "cake_type", "message")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("name", "phone", "cake_type", "required_date", "message", "created_at")
    fieldsets = (
        ("Customer Details", {
            "fields": ("name", "phone"),
        }),
        ("Order Details", {
            "fields": ("cake_type", "required_date", "message"),
        }),
        ("Status", {
            "fields": ("status",),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
