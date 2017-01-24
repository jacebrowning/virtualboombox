from django.db import models
from django.utils import timezone


class Song(models.Model):
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'"{self.title}" by {self.artist}'
