from django.urls import path
from .views import MediaListAPIView

urlpatterns = [
    path('api/gallery/', MediaListAPIView.as_view(), name='api-gallery-list'),
]
