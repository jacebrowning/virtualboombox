import logging

from django.shortcuts import reverse, render, redirect
from django.conf import settings

import pylast

from .models import Account, Song


log = logging.getLogger(__name__)


def index(request):
    context = dict(
        username=request.session.get('username'),
        lastfm_api_key=settings.LASTFM_API_KEY,
        lastfm_callback_url=request.build_absolute_uri(reverse('login')),
        songs=Song.objects.order_by('-date'),
    )

    return render(request, 'index.html', context)


def login(request):
    token = request.GET.get('token')

    account = Account.from_token(token)
    if account:
        request.session['username'] = account.username
    else:
        log.critical("TODO: show error message")

    return redirect('index')
