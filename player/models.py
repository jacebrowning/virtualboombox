from datetime import datetime
import logging

from django.db import models
from django.conf import settings
from django.utils import timezone

import pylast
import pytz


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
        """Retrieve an existing account or create a new one."""
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
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    @classmethod
    def from_account(cls, account):
        """Initialize a new song or update an existing song without saving."""
        log.debug(f"Adding songs from '{account.username}'...")

        network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET,
        )

        user = pylast.User(account.username, network)
        try:
            username = user.get_name(properly_capitalized=True)
        except pylast.WSError as exc:
            log.debug(exc)
            return None

        track = user.get_now_playing()
        if track:
            song, new = cls._get_or_init(track, account)
            if new:
                log.info(f"Added now playing from {username}: {song}")
            else:
                log.debug(f"Updated now playing from {username}: {song}")
            song.date = timezone.now()
            return song

        played_tracks = user.get_recent_tracks()
        if played_tracks:
            song, new = cls._get_or_init(played_tracks[0].track, account)
            if new:
                log.info(f"Added last track from {username}: {song}")
            else:
                log.debug(f"Updated last track from {username}: {song}")
            song.date = cls._timestamp_to_datetime(played_tracks[0].timestamp)
            return song

        return None

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f'"{self.title}" by {self.artist}'

    @classmethod
    def _get_or_init(cls, track, account):
        kwargs = dict(
            artist=track.artist,
            title=track.title,
            account=account,
        )
        try:
            obj = cls.objects.get(**kwargs)
            created = False
        except cls.DoesNotExist:
            obj = cls(**kwargs)
            created = True

        obj.latitude = account.latitude
        obj.longitude = account.longitude

        return obj, created

    @staticmethod
    def _timestamp_to_datetime(value):
        """Convert a UTC timestamp to a datetime object."""
        return datetime.utcfromtimestamp(int(value)).replace(tzinfo=pytz.utc)
