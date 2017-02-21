import time

from django.core.management.base import BaseCommand

from player.models import Account, Song


class Command(BaseCommand):
    help = "Adds the latest playing song from every account"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        interval = 0
        for account in Account.objects.order_by('-date'):
            song = Song.from_account(account)
            if song:
                song.update()
                song.save()

                # YouTube API quota: 1,000,000 points / 24 hours
                # Cost per query: 100 points
                # Seconds in a day: 24 * 60 * 60 = 86,400 seconds
                # Minimum seconds between requests: 86.4
                delay = 60 * 1.5
                time.sleep(delay)
                interval += delay
                if interval > 60 * 4:
                    break
