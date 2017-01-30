import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from player.models import Account, Song

from .serializers import SongSerializer, NextSerializer
from .utils import haversine


log = logging.getLogger(__name__)


class SongViewSet(viewsets.ModelViewSet):

    queryset = Song.objects.all()
    serializer_class = SongSerializer


class NextViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = NextSerializer

    @csrf_exempt
    def create(self, request):
        username = self._get_username(request)
        location = self._get_location(request)

        if username:
            self._update_account(username, location)

        song, distance = self._get_next_song(location)
        data = dict(
            artist=song.artist,
            title=song.title,
            distance=distance,
        )

        return Response(data, status=200)

    @staticmethod
    def _get_username(request):
        username = request.POST.get('username')
        if username:
            log.info("Account specified: %s", username)
            return username

        username = request.session.get('username')
        if username:
            log.info("Account loaded from session: %s", username)
            return username

        log.debug("User is not logged in")
        return None

    @staticmethod
    def _get_location(request):
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        log.info("Location specified: %s, %s", latitude, longitude)
        return latitude, longitude

    @staticmethod
    def _update_account(username, location):
        log.debug("Updating account location...")
        account = Account.objects.filter(username=username).first()
        if account:
            account.latitude = location[0]
            account.longitude = location[1]
            account.save()
        else:
            log.warning("No matching account for username: %r", username)

    @staticmethod
    def _get_next_song(location):
        # TODO: find the best matching song
        for song in Song.objects.all():
            base = (song.latitude, song.longitude)
            distance = haversine(location, base)
            return song, distance
