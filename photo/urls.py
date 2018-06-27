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
from django.contrib.auth import views as auth_views
from rest_framework import routers

from . import views
from . import rest

from photo.models import Photo

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('photo', rest.PhotoViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('photos', views.PhotoList.as_view()),
    path('upload', views.upload, name='upload'),

    path('api/', include(router.urls)),

    #path('login', auth_views.LoginView.as_view()),
    #path('<int:test_id>', views.detail, name='detail'),
]
