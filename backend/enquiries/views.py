from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Enquiry
from .serializers import EnquiryCreateSerializer


class EnquiryCreateAPIView(generics.CreateAPIView):
    """
    POST /api/enquiries/
    Public endpoint — saves a customer enquiry to PostgreSQL.
    Returns 201 on success. No authentication required.
    GET is not allowed (list is admin-only via Django Admin).
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquiryCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # status defaults to 'pending' at model level
        return Response(
            {"success": True, "message": "Enquiry received. We will contact you shortly!"},
            status=status.HTTP_201_CREATED,
        )
