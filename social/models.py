from enum import Enum

from django.db import models
from django.utils import timezone

from player.models import Song


class CannedReaction(Enum):
    LOVE = '<span class="glyphicon glyphicon-heart"></span>'
    LIKE = '<span class="glyphicon glyphicon-thumbs-up"></span>'
    HATE = '<span class="glyphicon glyphicon-thumbs-down"></span>'


class Reaction(models.Model):

    comment = models.CharField(max_length=500)
    song = models.ForeignKey(Song, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, *args, **kwargs):
        reaction = cls(*args, **kwargs)

        try:
            reaction.comment = CannedReaction[reaction.comment].value
        except KeyError:
            for bad, good in {('<', '&lt;'), ('>', '&gt;')}:
                reaction.comment = reaction.comment.replace(bad, good)

        return reaction

    @property
    def song_ref(self):
        return self.song.ref

    def __str__(self):
        return self.comment
