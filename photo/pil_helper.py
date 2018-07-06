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

import PIL, PIL.Image, PIL.ExifTags, PIL.TiffTags

def get_exif_tags(img):
    try:
        raw_exif = img._getexif()
        if not raw_exif:
            return {}
    except AttributeError:
        return {}

    tags = {}
    for key, value in raw_exif.items():
        key = PIL.ExifTags.TAGS.get(key, key)
        tags[key] = value
    return tags

def get_image_rotation(img):
    """Returns the rotation angle (in degrees), horizontal and vertical flip
    of the image according to any embedded tags"""

    angle = 0
    h_flip = False
    v_flip = False
    
    # Check the exif tags
    tags = get_exif_tags(img)
    try:
        rot = tags['Orientation']
        print(tags)
    except KeyError:
        pass
    else:
        if rot == 1:
            rot = 0;
        elif rot == 2:
            h_flip = True
        elif rot == 3:
            angle = 180
        elif rot == 4:
            angle = 180
            h_flip = True
        elif rot == 5:
            angle = 90
            h_flip = True
        elif rot == 6:
            angle = 90
        elif rot == 7:
            angle = 270
            h_flip = true
        elif rot == 8:
            angle = 270

    # TODO - handle tiff image rotation
    # ...

    return (-angle, h_flip, v_flip)
