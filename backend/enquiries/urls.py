from django.urls import path
from .views import EnquiryCreateAPIView

urlpatterns = [
    # POST only — customers submit enquiries
    # GET /api/enquiries/ is intentionally NOT exposed (use Django Admin)
    path("api/enquiries/", EnquiryCreateAPIView.as_view(), name="api-enquiry-create"),
]
