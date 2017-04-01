# pylint: disable=unused-variable,expression-not-assigned,redefined-outer-name,singleton-comparison

import pytest
from expecter import expect

from player.models import Song

from ..models import Reaction


def describe_reaction():

    @pytest.fixture
    def reaction(song):
        return Reaction(
            song=song,
            comment="Great song!",
        )

    @pytest.fixture
    def song():
        return Song()

    def describe_create():

        def it_replaces_unsafe_characters(song):
            unsafe = '<script>alert("Hello, world!");</script>'
            reaction = Reaction.create(song=song, comment=unsafe)

            expect(reaction.comment) == \
                '&lt;script&gt;alert("Hello, world!");&lt;/script&gt;'

        def it_styles_reactions(song):
            reaction = Reaction.create(song=song, comment='LOVE',)

            expect(reaction.comment) == \
                '<span class="glyphicon glyphicon-heart"></span>'

    def describe_str():

        def it_uses_the_message(reaction):
            expect(str(reaction)) == "Great song!"
