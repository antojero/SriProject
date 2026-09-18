from rest_framework import generics
from .models import Cake
from .serializers import CakeSerializer

class CakeListAPIView(generics.ListCreateAPIView):
    serializer_class = CakeSerializer

    def get_queryset(self):
        queryset = Cake.objects.filter(published=True)
        featured = self.request.query_params.get('featured')

        if featured == 'true':
            queryset = queryset.filter(featured=True)

        return queryset
