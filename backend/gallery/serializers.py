from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            'id',
            'type',
            'category',
            'title',
            'file',
            'src',
            'instagram_url',
            'created_at'
        ]

    def get_src(self, obj):
        request = self.context.get('request')
        if obj.file:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return ""
