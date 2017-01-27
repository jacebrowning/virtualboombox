import logging

from django.shortcuts import render, redirect
from django.conf import settings

import pylast

from .models import Song


log = logging.getLogger(__name__)


def index(request,):
    context = dict(
        username=request.session.get('username'),
        api_key=settings.LASTFM_API_KEY,
        songs=Song.objects.order_by('date'),
    )

    return render(request, 'index.html', context)


def login(request):
    token = request.GET.get('token')
    log.info("Last.fm token: %s", token)

    network = pylast.LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_API_SECRET,
    )
    request = pylast._Request(network, 'auth.getSession', {'token': token})
    request.sign_it()
    try:
        doc = request.execute()
    except pylast.WSError as exc:
        log.error(exc)
        # TODO: show error message
    else:
        username = doc.getElementsByTagName('name')[0].firstChild.data
        log.info("Last.fm username: %s", username)
        request.session['username'] = username

    return redirect('index')
