
from .models import Photo
from rest_framework import serializers, viewsets

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'image_width', 'image_height')
        read_only_fields = ('image_width', 'image_height')

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
