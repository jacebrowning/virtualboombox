from django.conf.urls import url, include
from rest_framework import routers, serializers

from . import views


router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'next', views.NextViewSet, base_name='next')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls')),
]
