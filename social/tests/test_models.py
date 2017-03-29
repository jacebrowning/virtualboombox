# pylint: disable=unused-variable,expression-not-assigned,redefined-outer-name,singleton-comparison

from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from expecter import expect

from player.models import Song

from ..models import Reaction


def describe_reaction():

    @pytest.fixture
    def reaction():
        return Reaction(
            song=Song(),
            comment="Great song!",
        )

    def describe_str():

        def it_uses_the_message(reaction):
            expect(str(reaction)) == "Great song!"
