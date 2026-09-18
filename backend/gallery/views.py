from rest_framework import generics
from .models import Media
from .serializers import MediaSerializer

class MediaListAPIView(generics.ListCreateAPIView):
    serializer_class = MediaSerializer

    def get_queryset(self):
        queryset = Media.objects.filter(published=True)
        category = self.request.query_params.get('category')
        if category and category != 'All':
            queryset = queryset.filter(category__iexact=category)
        return queryset
