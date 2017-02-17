import re
from datetime import datetime, timedelta
import logging

from django.db import models
from django.conf import settings
from django.utils import timezone

import pylast
import pytz
from apiclient.discovery import build


DEFAULT_LOCATION = (-48.876667, -123.393333)  # Oceanic Pole of Inaccessibility

log = logging.getLogger(__name__)


class Location(models.Model):
    """Geographic coordinates."""

    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   default=DEFAULT_LOCATION[0])
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    default=DEFAULT_LOCATION[1])
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    @property
    def maps_url(self):
        return ("https://www.google.com/maps/"
                f"@{self.latitude:.4f},{self.longitude:.4f},10z")

    class Meta:
        abstract = True


class Account(Location):
    """Last.fm account information and metadata."""

    username = models.CharField(max_length=50, unique=True)

    @classmethod
    def from_token(cls, token):
        """Retrieve an existing account or create a new one."""
        if not token:
            log.error("No token provided")
            return None

        log.info("Last.fm token: %s", token)
        username = cls._get_username_from_token(token)
        if not username:
            log.error("No account for token: %s", token)
            return None

        account, created = cls.objects.get_or_create(username=username)

        if created:
            log.info("Added account: %s", account)
        else:
            log.info("Found account: %s", account)

        return account

    def __str__(self):
        location = super().__str__()
        return f"{self.username} @ {location}"

    def _set_location(self, pair):
        self.latitude, self.longitude = pair
        self.date = timezone.now()
    location = property(fset=_set_location)

    @staticmethod
    def _get_username_from_token(token):
        try:
            network = pylast.LastFMNetwork(
                api_key=settings.LASTFM_API_KEY,
                api_secret=settings.LASTFM_API_SECRET,
                token=token
            )
        except pylast.WSError as exc:
            log.error(exc)
            return None
        else:
            return network.get_authenticated_user().get_name()


class Song(Location):
    """Played song with location information."""

    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    youtube_url = models.URLField(null=True)

    RE_PODCAST = re.compile("episode\s+\d+", re.IGNORECASE)

    class Meta:
        unique_together = ('artist', 'title', 'account')

    @classmethod
    def from_account(cls, account):
        """Initialize a new song or update an existing song without saving."""
        log.debug(f"Adding songs from '{account.username}'...")

        time.sleep(1)  # quota rate limiter

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

    @property
    def location(self):
        return float(self.latitude), float(self.longitude)

    @property
    def unknown(self):
        return not all((
            self.youtube_url,
            not self.RE_PODCAST.search(self.title),
        ))

    @property
    def stale(self):
        return timezone.now() - self.date > timedelta(hours=6)

    @property
    def lastfm_url(self):
        artist = self.artist.replace(' ', '+')
        title = self.title.replace(' ', '+')
        return f"http://www.last.fm/music/{artist}/_/{title}"

    def update(self):
        """Update all externally computed properties."""
        return any((
            self.update_youtube_url(),
        ))

    def update_youtube_url(self):
        """Update the YouTube URL if not set."""
        if self.youtube_url:
            return False

        time.sleep(1)  # quota rate limiter

        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

        query = f"{self.artist} - {self.title}"
        response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=5
        ).execute()

        for result in response.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                key = result['id']['videoId']
                self.youtube_url = f"https://www.youtube.com/v/{key}"
                log.info("%r => %s", query, self.youtube_url)
                return True

        log.warning("%r => (no YouTube results)", query)

        return False

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
