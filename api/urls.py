from django.conf.urls import url, include
from rest_framework import routers, serializers

from . import views


router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'queue', views.QueuedSongViewSet, base_name='queue')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls')),
]
