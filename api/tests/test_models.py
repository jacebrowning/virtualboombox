from unittest.mock import Mock

import pytest
from expecter import expect

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
                artist="John Mayer",
                title="No Such Thing",
                youtube_url="http://example.com",
            ),
            that_location=irvine_ca,
            this_location=grand_rapids_mi,
        )

    def describe_distance():

        def when_near(song):
            song.this_location = song.that_location

            expect(song.distance) == 0.0

        def when_distant(song):
            expect(song.distance) == 1841.7935937669608

    def describe_angle():

        def when_near(song):
            song.this_location = song.that_location

            expect(song.angle) == 0.0

        def when_distant(song):
            expect(song.angle) == 260.4110953861232

    def describe_data():

        def it_optimizes_for_clients(song):
            expect(song.data) == {
                'artist': 'John Mayer',
                'title': 'No Such Thing',
                'youtube_url': 'http://example.com',
                'miles': '1841.8',
                'degrees': 260.4110953861232,
            }
