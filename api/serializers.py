from rest_framework import serializers

from player.models import Song


class SongSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Song
        fields = ('url', 'artist', 'title', 'latitude', 'longitude', 'date')


class NextSerializer(serializers.Serializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    username = serializers.CharField(required=False)