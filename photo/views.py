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

from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from photo.models import Photo
from photo.forms import PhotoForm

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
            form.save()
            return HttpResponseRedirect('/')

    else:
        form = PhotoForm()

    return render(request, 'photo/upload.html', {
        'form' : form,
    })

