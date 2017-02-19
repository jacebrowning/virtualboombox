from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from player.models import Account, Song


class Command(BaseCommand):
    help = "Generate data for manual testing"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        Account.objects.get_or_create(username='justus87')

        a, _ = Account.objects.get_or_create(username='aliasguru')
        a.latitude = 33.670348
        a.longitude = -117.775990
        a.save()

        a, _ = Account.objects.get_or_create(username='thecreepr')
        a.latitude = 42.909358
        a.longitude = -85.753993
        a.save()

        Account.objects.get_or_create(username='_invalid')

        Song.objects.get_or_create(
            artist="The Beatles",
            title="Come Together",
            date=timezone.now() - timedelta(days=4),
        )

        Song.objects.get_or_create(
            artist="this_is_an_unknown_artist",
            title="this_is_an_unknown_title",
            date=timezone.now() - timedelta(days=3),
        )

        Song.objects.get_or_create(
            artist="An Old Artist",
            title="And Old Title",
            date=timezone.now() - timedelta(days=30),
        )
