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
                "https://www.google.com/maps/@1.2000,-3.4000,19z"


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


def describe_song():

    @pytest.fixture
    def song():
        return Song(artist="The Bars", title="Foo", latitude=1, longitude=2)

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

        def when_no_links(song):
            expect(song.unknown) == True

    def describe_stale():

        def when_new(song):
            song.date = timezone.now() - timedelta(days=1)

            expect(song.stale) == False

        def when_old(song):
            song.date = timezone.now() - timedelta(days=8)

            expect(song.stale) == True
