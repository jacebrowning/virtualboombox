import time

from django.core.management.base import BaseCommand
from django.conf import settings

from player.models import Account, Song


class Command(BaseCommand):
    help = "Adds the latest playing song from every account"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        for account in Account.objects.order_by('-date'):
            song = Song.from_account(account)

            if song:
                if song.update():
                    time.sleep(settings.YOUTUBE_API_DELAY)

            if song:
                song.save()
