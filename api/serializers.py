from rest_framework import serializers

from player.models import Song


class SongSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Song
        fields = ('url', 'artist', 'title', 'latitude', 'longitude', 'date')
