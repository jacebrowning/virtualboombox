import pytest
from expecter import expect

from ..models import Account, Song


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
        return Song(artist="The Bars", title="Foo")

    def describe_str():

        def with_nominal_values(song):
            expect(str(song)) == '"Foo" by The Bars'
