from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "cake_type", "required_date", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone", "message")
