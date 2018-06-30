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

from django.db import models

# Create your models here.
class Photo(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        width_field='image_width',
        height_field='image_height')

    comment = models.CharField(default="", max_length=100)

    image_width = models.IntegerField()
    image_height = models.IntegerField()
