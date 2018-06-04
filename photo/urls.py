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
