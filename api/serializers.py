from rest_framework import serializers

from player.models import Account, Song


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'latitude', 'longitude')


class SongSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Song
        fields = ('url', 'artist', 'title', 'latitude', 'longitude', 'date')


class QueueSerializer(serializers.Serializer):  # pylint: disable=abstract-method

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    username = serializers.CharField(required=False)
    limit = serializers.IntegerField(min_value=1, default=10)
