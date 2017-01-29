from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from . import views


urlpatterns = [
    url(r'^auth/', include('rest_framework.urls')),
    url(r'^songs/$', views.SongList.as_view()),
    url(r'^songs/(?P<pk>[0-9]+)/$', views.SongDetail.as_view()),
]
