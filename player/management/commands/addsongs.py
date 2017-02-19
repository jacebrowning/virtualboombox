from django.core.management.base import BaseCommand

from player.models import Account, Song


class Command(BaseCommand):
    help = "Adds the latest playing song from every account"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        for account in Account.objects.all():
            song = Song.from_account(account)
            if song:
                song.update()
                song.save()
