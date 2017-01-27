import pytest
from expecter import expect

from ..models import Song


def describe_song():

    @pytest.fixture
    def song():
        return Song(artist="The Bars", title="Foo")

    def describe_str():

        def when_nominal(song):
            expect(str(song)) == '"Foo" by The Bars'
