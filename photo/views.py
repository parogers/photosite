
from django.shortcuts import render
from django.http import HttpResponse
from photo.models import Photo

def index(request):
    return render(request, 'photo/index.html', {
        'photo_list' : Photo.objects.all(),
    })

