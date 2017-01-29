from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from player.models import Account, Song


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('artist', 'title', 'latitude', 'longitude', 'date')


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls')),
]
