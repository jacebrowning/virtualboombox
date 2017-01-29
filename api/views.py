import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from player.models import Account, Song

from .serializers import SongSerializer, NextSerializer


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
        log.info("Updating account location...")

        username = request.POST.get('username')
        if username:
            log.info("Account specified: %s", username)
        else:
            username = request.session.get('username')
            log.info("Account loaded from session: %s", username)

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        log.info("Location specified: %s, %s", latitude, longitude)

        account = Account.objects.filter(username=username).first()
        if account:
            account.latitude = latitude
            account.longitude = longitude
            account.save()
        else:
            log.warning("No matching account for username: %r", username)

        return Response({})
