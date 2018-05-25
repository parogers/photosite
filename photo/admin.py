from django.contrib import admin
from . import models

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image')

admin.site.register(models.Photo, PhotoAdmin)
