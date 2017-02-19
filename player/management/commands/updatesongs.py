from django.core.management.base import BaseCommand

from player.models import Song


class Command(BaseCommand):
    help = "Updates metadata for all songs"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        for song in Song.objects.order_by('-date'):
            if song.update():
                song.save()
