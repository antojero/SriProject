from rest_framework import serializers
from .models import Cake

class CakeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Cake
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'image_url',
            'featured',
            'published',
            'created_at'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return ""
