from rest_framework import serializers

from player.models import Account, Song
from social.models import Reaction


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
    weightDistance = serializers.FloatField(default=0.5)
    weightTime = serializers.FloatField(default=0.5)


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('comment', 'song')
