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
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from photo.models import Photo
from photo.forms import PhotoForm
from . import pil_helper

PREVIEW_WIDTH = 100
PREVIEW_HEIGHT = 100

class PhotoList(ListView):
    model = Photo
    template_name = 'photo/index.html'
    context_object_name = 'photo_list'

def index(request):
    return render(request, 'photo/index.html', {
        'photo_list' : Photo.objects.all(),
        'user' : request.user,
    })

@login_required
def upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()

            fs = FileSystemStorage()

            # Generate a preview image and dump it into a bytes buffer
            img = PIL.Image.open(fs.open(photo.image.name))
            img.thumbnail((PREVIEW_WIDTH, PREVIEW_HEIGHT))
            img_file = io.BytesIO(img.tobytes())

            # Handle image rotation specified via exif
            rot, h_flip, v_flip = pil_helper.get_image_rotation(img)
            print(rot)
            if rot:
                img = img.rotate(rot)

            buf = io.BytesIO()
            img.save(buf, 'png')

            # Save the image buffer to default file storage
            preview_path = fs.get_available_name(photo.image.name)
            fs.save(preview_path, buf)
            photo.preview = preview_path
            photo.preview_width = img.width
            photo.preview_height = img.height
            photo.save()
            
            return HttpResponseRedirect('/')

    else:
        form = PhotoForm()

    return render(request, 'photo/upload.html', {
        'form' : form,
    })

