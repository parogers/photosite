from django.db import models

# Create your models here.
class Photo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        width_field='image_width',
        height_field='image_height')

    image_width = models.IntegerField()
    image_height = models.IntegerField()
