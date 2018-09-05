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

from django.urls import path, include

from . import rest

app_name = 'easyauth'
urlpatterns = [
    path('begin', rest.begin_registration, name='begin'),
    path('complete', rest.complete_registration, name='complete'),
    path('obtain-access-code/',
         rest.obtain_access_code,
         name='obtain_access_code'),
    path('obtain-access-code/<str:token>',
         rest.obtain_access_code,
         name='obtain_access_code'),
]
