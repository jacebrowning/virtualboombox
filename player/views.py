from django.shortcuts import render

from .models import Song


def index(request):
    songs = Song.objects.order_by('date')
    return render(request, 'index.html', {'songs': songs})
