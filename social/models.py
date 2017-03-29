from django.db import models
from django.utils import timezone

from player.models import Song


class Reaction(models.Model):

    comment = models.CharField(max_length=500)
    song = models.ForeignKey(Song, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
