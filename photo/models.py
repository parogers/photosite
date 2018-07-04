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

import io
import PIL, PIL.Image
from django.db import models
from django.core.files.storage import FileSystemStorage

from . import pil_helper

PREVIEW_WIDTH = 300
PREVIEW_HEIGHT = 300

# Create your models here.
class Photo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        width_field='image_width',
        height_field='image_height')
    preview = models.ImageField(
        width_field='preview_width',
        height_field='preview_height',
        null=True)

    comment = models.CharField(default="", max_length=100)

    image_width = models.IntegerField()
    image_height = models.IntegerField()

    preview_width = models.IntegerField(default=0)
    preview_height = models.IntegerField(default=0)

    def generate_and_save_preview(self):
        fs = FileSystemStorage()

        # Generate a preview image and dump it into a bytes buffer
        img = PIL.Image.open(fs.open(self.image.name))
        img.thumbnail((PREVIEW_WIDTH, PREVIEW_HEIGHT))

        # Handle image rotation specified via exif
        rot, h_flip, v_flip = pil_helper.get_image_rotation(img)
        if rot:
            print(rot)
            img = img.rotate(rot)

        buf = io.BytesIO()
        img.save(buf, 'png')

        # Save the image buffer to default file storage
        preview_path = fs.get_available_name(self.image.name)
        fs.save(preview_path, buf)
        self.preview = preview_path
        self.preview_width = img.width
        self.preview_height = img.height
        self.save()
