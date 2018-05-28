
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from photo.models import Photo
from photo.forms import PhotoForm

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

