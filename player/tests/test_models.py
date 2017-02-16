from datetime import timedelta

import pytest
from expecter import expect
from django.utils import timezone

from ..models import Location, Account, Song


def describe_location():

    @pytest.fixture
    def location():
        return Location(latitude=1.2, longitude=-3.4)

    def describe_maps_url():

        def it_uses_google_maps(location):
            expect(location.maps_url) == \
                "https://www.google.com/maps/@1.2000,-3.4000,10z"


def describe_account():

    @pytest.fixture
    def account():
        return Account(username="foobar")

    def describe_str():

        def with_default_location(account):
            expect(str(account)) == "foobar @ (-48.876667, -123.393333)"

        def with_updated_location(account):
            account.latitude = 1.2
            account.longitude = -3.4

            expect(str(account)) == "foobar @ (1.2, -3.4)"

    def describe_location():

        def it_updates_the_date(account):
            initial_date = account.date

            account.location = (1, 2)

            expect(account.latitude) == 1.0
            expect(account.longitude) == 2.0
            expect(account.date) > initial_date


def describe_song():

    @pytest.fixture
    def song():
        return Song(
            artist="The Bars", title="Foo",
            youtube_url="http://example.com",
            latitude=1, longitude=2,
        )

    def describe_str():

        def it_uses_the_name(song):
            expect(str(song)) == '"Foo" by The Bars'

    def describe_name():

        def it_joins_the_artist_and_title(song):
            expect(song.name) == '"Foo" by The Bars'

    def describe_location():

        def is_a_tuple(song):
            expect(song.location) == (1.0, 2.0)

    def describe_unknown():

        def when_no_youtube_url(song):
            song.youtube_url = None

            expect(song.unknown) == True

        def when_podcast(song):
            song.title = "Episode 42: Foo"

            expect(song.unknown) == True

    def describe_stale():

        def when_new(song):
            song.date = timezone.now() - timedelta(hours=5.9)

            expect(song.stale) == False

        def when_old(song):
            song.date = timezone.now() - timedelta(hours=6.1)

            expect(song.stale) == True

    def describe_lastfm_url():

        def is_based_on_artist_and_title(song):
            expect(song.lastfm_url) == \
                "http://www.last.fm/music/The+Bars/_/Foo"
