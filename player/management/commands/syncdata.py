import time
import logging

from django.core.management.base import BaseCommand

from player.models import Account, Song


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Synchronize data with external APIs"

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=None)
        parser.add_argument('--loop', action='store_true')

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        limit = kwargs['limit']
        once = not kwargs['loop']

        while True:
            self.add_songs()
            self.update_songs()
            self.prune_songs(limit)

            if once:
                break

    @staticmethod
    def add_songs():
        start = time.time()

        for account in Account.objects.order_by('-date'):
            song = Song.from_account(account)
            if song and song.update():
                song.save()

            if time.time() - start > 60 * 4:
                log.warning("Breaking early to cycle users")
                break

    @staticmethod
    def update_songs():
        for song in Song.objects.order_by('-date'):
            if song.update():
                song.save()

    @staticmethod
    def prune_songs(limit):
        count = Song.objects.count()

        for song in Song.objects.order_by('-date'):

            if limit and count <= limit:
                log.warning(f"Only {count} songs in queue")
                return

            if song.unknown:
                log.info("Deleting unidentifiable song: %s", song)
                song.delete()
                count -= 1

            elif song.stale:
                log.info("Deleting stale song: %s", song)
                song.delete()
                count -= 1
