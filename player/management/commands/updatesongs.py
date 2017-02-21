import time

from django.core.management.base import BaseCommand
from django.conf import settings

from player.models import Song


class Command(BaseCommand):
    help = "Updates metadata for all songs"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        for song in Song.objects.order_by('-date'):
            if song.update():
                song.save()

                time.sleep(settings.YOUTUBE_API_DELAY)
