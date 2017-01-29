import logging

from django.db import models
from django.conf import settings
from django.utils import timezone

import pylast


DEFAULT_LOCATION = (-48.876667, -123.393333)  # Oceanic Pole of Inaccessibility

log = logging.getLogger(__name__)


class Location(models.Model):
    """Geographic coordinates."""

    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   default=DEFAULT_LOCATION[0])
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    default=DEFAULT_LOCATION[1])

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    @property
    def url(self):
        return ("https://www.google.com/maps/"
                f"@{self.latitude:.4f},{self.longitude:.4f},19z")

    class Meta:
        abstract = True


class Account(Location):
    """Last.fm account information and metadata."""

    username = models.CharField(max_length=50)

    @classmethod
    def from_token(cls, token):
        log.info("Last.fm token: %s", token)
        username = cls._get_username_from_token(token)

        account, created = cls.objects.get_or_create(username=username)

        if created:
            log.info("Added account: %s", account)
        else:
            log.info("Found account: %s", account)

        return account

    @staticmethod
    def _get_username_from_token(token):
        network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET,
        )

        call = pylast._Request(network, 'auth.getSession', {'token': token})
        call.sign_it()

        try:
            xml = call.execute()
        except pylast.WSError as exc:
            log.error(exc)
            username = None
        else:
            username = xml.getElementsByTagName('name')[0].firstChild.data

        return username

    def __str__(self):
        location = super().__str__()
        return f"{self.username} @ {location}"


class Song(Location):
    """Played song with location information."""

    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f'"{self.title}" by {self.artist}'
