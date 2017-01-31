from django.core.management.base import BaseCommand

from player.models import Account, Song


class Command(BaseCommand):
    help = "Generate data for manual testing"

    def handle(self, *args, **kwargs):
        Account.objects.get_or_create(username='justus87')

        a, _ = Account.objects.get_or_create(username='aliasguru')
        a.latitude = 33.670348
        a.longitude = 117.775990
        a.save()

        a, _ = Account.objects.get_or_create(username='thecreepr')
        a.latitude = 42.909358
        a.longitude = -85.753993
        a.save()

        Account.objects.get_or_create(username='_invalid')

        s = Song.objects.get_or_create(
            artist="The Beatles",
            title="Come Together",
        )
