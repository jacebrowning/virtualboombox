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
    limit = serializers.IntegerField(min_value=1, default=1)
