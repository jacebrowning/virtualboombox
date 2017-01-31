from rest_framework import serializers

from player.models import Song


class SongSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Song
        fields = ('url', 'artist', 'title', 'latitude', 'longitude', 'date')


class QueueRequestSerializer(serializers.Serializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    username = serializers.CharField(required=False)


class QueuedSongSerializer(serializers.Serializer):

    artist = serializers.CharField()
    title = serializers.CharField()
    distance = serializers.FloatField()
