from django.urls import path
from .views import CakeListAPIView

urlpatterns = [
    path('api/cakes/', CakeListAPIView.as_view(), name='api-cake-list'),
]
