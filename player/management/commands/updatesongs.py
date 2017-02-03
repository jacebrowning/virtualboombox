import time
import logging

from django.core.management.base import BaseCommand

from player.models import Account, Song


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates metadata for all songs"

    def handle(self, **options):
        for song in Song.objects.order_by('-date'):
            if song.update():
                song.save()
                time.sleep(1)
