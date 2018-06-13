
from .models import Photo
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'comment', 'image_width', 'image_height')
        read_only_fields = ('image_width', 'image_height')

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # detail=False => this action can be called without referring to a photo
    # object (eg GET /api/photo/something)
    @action(detail=False, methods=['get'])
    def something(self, request):
        return Response('hello world')
