from rest_framework import serializers
from .models import Enquiry


class EnquiryCreateSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/enquiries/ — customer-facing enquiry submission.
    Only exposes writable fields. status is server-controlled (defaults to 'pending').
    """
    class Meta:
        model = Enquiry
        fields = ["name", "phone", "cake_type", "required_date", "message"]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()

    def validate_phone(self, value):
        digits = "".join(filter(str.isdigit, value))
        if len(digits) < 7:
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value.strip()
