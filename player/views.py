from django.shortcuts import render, redirect
from django.conf import settings

from pylast import LastFMNetwork, _Request

from .models import Song


def index(request, username=None):
    context = dict(
        username=username,
        api_key=settings.LASTFM_API_KEY,
        songs=Song.objects.order_by('date'),
    )

    return render(request, 'index.html', context)


def login(request):
    token = request.GET.get('token')

    network = LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_API_SECRET,
    )
    request = _Request(network, 'auth.getSession', {'token': token})
    request.sign_it()
    doc = request.execute()

    username = doc.getElementsByTagName('name')[0].firstChild.data
    print("Last.fm username: " + username)

    return redirect('index', username=username)
