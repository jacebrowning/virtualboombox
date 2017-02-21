import logging

from django.core.management.base import BaseCommand

from player.models import Song


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Deletes unknown and stale songs"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        count = Song.objects.count()
        if count < 250:
            log.warning("Only f{count} songs")
            return
        for song in Song.objects.order_by('-date'):
            if song.unknown:
                log.info("Deleting unidentifiable song: %s", song)
                song.delete()
            elif song.stale:
                log.info("Deleting stale song: %s", song)
                song.delete()
