import time

from django.core.management.base import BaseCommand

from player.models import Account, Song


class Command(BaseCommand):
    help = "Adds the latest playing song from every account"

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help="Run the command continuously",
        )

    def handle(self, **options):
        while True:
            for account in Account.objects.all():
                song = Song.from_account(account)
                if song:
                    song.save()

                time.sleep(1)

            if not options['loop']:
                break

