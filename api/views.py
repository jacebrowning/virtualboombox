import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from player.models import Account, Song

from .permissions import AllowAnonCreate
from .serializers import AccountSerializer, SongSerializer, QueueSerializer
from .models import QueuedSong


log = logging.getLogger(__name__)


class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAnonCreate]

    def list(self, request):
        if request.user.is_superuser:
            return super().list(request)
        else:
            return Response([])

    @csrf_exempt
    def create(self, request):
        account = get_object_or_404(Account, username=request.POST['username'])

        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class SongViewSet(viewsets.ModelViewSet):

    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAnonCreate]

    def list(self, request):
        if request.user.is_superuser:
            return super().list(request)
        else:
            return Response([])


class QueuedViewSet(viewsets.ViewSet):

    serializer_class = QueueSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def create(self, request):
        username = self._get_username(request)
        location = self._get_location(request)

        if username:
            self._update_account(username, location)

        songs = self._get_songs(request, username, location)

        return Response([s.data for s in songs])

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
        # TODO: require latitude and longitude, fail on blanks
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        log.info("Location specified: %s, %s", latitude, longitude)
        return latitude, longitude

    @staticmethod
    def _update_account(username, location):
        log.debug("Updating account location...")

        account = Account.objects.filter(username=username).first()
        if not account:
            log.warning("No matching account for username: %r", username)
            return

        account.latitude = location[0]
        account.longitude = location[1]
        account.save()

    @classmethod
    def _get_songs(cls, request, username, location):
        played_song_ids = request.session.get('played_song_ids', [])
        limit = int(request.POST.get('limit') or 1)

        result = cls._run_query(username, played_song_ids, location, limit)
        songs = sorted(result, key=lambda x: x.distance)
        assert songs, "No songs available"  # TODO: show a message to the user?

        log.info("Nearest song: %s @ %s", songs[0].distance, songs[0].angle)
        played_song_ids.append(songs[0].id)
        request.session['played_song_ids'] = played_song_ids

        return songs

    @staticmethod
    def _run_query(username, played_song_ids, location, limit):
        count = 0
        for song in Song.objects \
                .exclude(account__username=username).order_by('-date'):

            if song.id in played_song_ids:
                log.debug("Already played: %s", song)
                continue

            yield QueuedSong(song, location)

            count += 1
            if count >= limit:
                return
