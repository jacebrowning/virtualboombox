import logging

from django.core.management.base import BaseCommand

from player.models import Account, Song


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Deletes unknown and stale songs"

    def handle(self, **options):
        for song in Song.objects.order_by('-date'):
            if song.unknown:
                log.info("Deleting unidentifiable song: %s", song)
                song.delete()
            if song.stale:
                log.info("Deleting stale song: %s", song)
                song.delete()
