# photosite - A minimalist django site for posting photos
# Copyright (C) 2018  Peter Rogers (peter.rogers@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Photo
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

import re
from io import BytesIO
import base64

class Base64ImageField(serializers.ImageField):
    """Override the default ImageField implementation to allow for images
    submitted in base64 encoded format. (eg. data:image;base64,....)"""

    # In the serializer field class, to_internal_value converts user or form
    # submitted data into the relevant object representation.
    # (eg. date as a string => python datetime object)
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # Parse out the content type and encoded bytes
            m = re.match('^data:(.*?/.*?);base64,(.*)', data)
            if not m:
                self.fail('invalid', input=data)

            content_type, img_str = m.groups()
            base_type, img_ext = content_type.split('/')
            if base_type != 'image':
                self.fail('not_an_image', input=data)

            if img_ext not in ('jpg', 'png', 'gif'):
                self.fail('invalid_image_format', input=data)

            # Wrap the decoded bytes into a uploaded file object
            img_data = BytesIO(base64.b64decode(img_str))
            data = InMemoryUploadedFile(
                img_data, 'image', 'photo.' + img_ext,
                content_type, len(img_data.getbuffer()), 'UTF-8')

        return super().to_internal_value(data)

#class PhotoSerializer(serializers.Serializer):
#    comment = serializers.CharField(max_length=100)
#    image = Base64ImageField()
#    image_width = serializers.IntegerField()
#    image_height = serializers.IntegerField()
#
#    def create(self, validated_data):
#        return Photo(**validated_data)
#
#    def update(self, photo, validated_data):
#        photo.image = validated_data['image']
#        photo.comment = validated_data['comment']
#        photo.save()
#        return photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'comment', 'image_width', 'image_height')
        # Fields that are ignored during record updates
        read_only_fields = ('id', 'image_width', 'image_height')
    
    image = Base64ImageField()

# Provides CRUD operations for photo records
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # Authentication classes can be specified here, otherwise DRF will
    # use the defaults supplied under settings.REST_FRAMEWORK
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # detail=False => this action can be called without referring to a photo
    # object (eg GET /api/photo/something)
    @action(detail=False, methods=['get'])
    def something(self, request):
        return Response('hello world')

class TestViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(list(range(10)))

    def retrieve(self, request, pk=None):
        return Response(int(pk))

    def update(self, request, pk=None):
        return Response('updated')

    def create(self, request):
        print('Create with', request.data)
        return Response('created')

    def destroy(self, request, pk=None):
        return Response('deleted')
