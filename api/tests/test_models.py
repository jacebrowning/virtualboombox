# pylint: disable=unused-variable,expression-not-assigned

from unittest.mock import Mock
from datetime import timedelta

import pytest
from expecter import expect
from django.utils import timezone

from ..models import QueuedSong


def describe_queued_song():

    @pytest.fixture
    def grand_rapids_mi():
        return (42.9634, -85.6681)

    @pytest.fixture
    def irvine_ca():
        return (33.6704, -117.776)

    @pytest.fixture
    def song(irvine_ca, grand_rapids_mi):
        return QueuedSong(
            song=Mock(
                id=42,
                artist="John Mayer",
                title="No Such Thing",
                lastfm_url="http://last.fm/foobar",
                youtube_url="http://youtube.com/foobar",
            ),
            that_location=irvine_ca,
            this_location=grand_rapids_mi,
        )

    def describe_id():

        def it_matches_the_song(song):
            expect(song.id) == 42

    def describe_elapsed_time():

        def when_live(song):
            song.song.date = timezone.now()

            expect(song.elapsed_time) == 0.0

        def when_recent(song):
            song.song.date = timezone.now() - timedelta(minutes=15)

            expect(song.elapsed_time) == 15.0

        def when_old(song):
            song.song.date = timezone.now() - timedelta(days=2)

            expect(song.elapsed_time) == 2880.0

    def describe_distance():

        def when_near(song):
            song.this_location = song.that_location

            expect(song.distance) == 0.0

        def when_far(song):
            expect(song.distance) == 1841.7935937669608

    def describe_score():

        def when_near_and_new(song):
            song.this_location = song.that_location
            song.elapsed_time = 4

            expect(song.score) == 1.0

        def when_near_and_old(song):
            song.this_location = song.that_location
            song.elapsed_time = 15

            expect(song.score) == 0.997

        def when_far_and_new(song):
            song.elapsed_time = 0

            expect(song.score) == 0.926

        def when_far_and_old(song):
            song.elapsed_time = 15

            expect(song.score) == 0.923

        def when_favoring_distance(song):
            song.elapsed_time = 15
            song.WEIGHT_DISTANCE = 1.0
            song.WEIGHT_TIME = 0.0

            expect(song.score) == 0.852

        def when_favoring_time(song):
            song.elapsed_time = 15
            song.WEIGHT_DISTANCE = 0.0
            song.WEIGHT_TIME = 1.0

            expect(song.score) == 0.993

    def describe_angle():

        def when_near(song):
            song.this_location = song.that_location

            expect(song.angle) == 0.0

        def when_far(song):
            expect(song.angle) == 260.4110953861232

    def describe_data():

        def it_optimizes_for_clients(song):
            expect(song.data) == {
                'id': 42,
                'artist': 'John Mayer',
                'title': 'No Such Thing',
                'lastfm_url': 'http://last.fm/foobar',
                'youtube_url': 'http://youtube.com/foobar',
                'miles': '1842',
                'degrees': 260.4110953861232,
            }

        def it_includes_decimals_on_smaller_distances(song):
            song.distance = 1.23

            expect(song.data['miles']) == '1.2'
