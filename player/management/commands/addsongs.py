import time
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from player.models import Account, Song


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Adds the latest playing song from every account"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        for account in Account.objects.order_by('-date'):
            song = Song.from_account(account)

            if song:
                song.save()

                if song.update():
                    if song.unknown:
                        log.info("Deleting unidentifiable song: %s", song)
                        song.delete()
                    else:
                        song.save()
                    time.sleep(settings.YOUTUBE_API_DELAY)
