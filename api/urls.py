from django.conf.urls import url, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='accounts')
router.register(r'songs', views.SongViewSet)
router.register(r'queue', views.QueuedViewSet, basename='queue')
router.register(r'reactions', views.ReactionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls')),
]
