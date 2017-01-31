from django.core.management.base import BaseCommand

from player.models import Account, Song


class Command(BaseCommand):
    help = "Generate data for manual testing"

    def handle(self, *args, **kwargs):
        account = Account.objects.get_or_create(username='justus87')
        Account.objects.get_or_create(username='aliasguru')
        Account.objects.get_or_create(username='thecreepr')
        Account.objects.get_or_create(username='_invalid')

        Song.objects.get_or_create(
            artist="The Beatles",
            title="Come Together",
        )
