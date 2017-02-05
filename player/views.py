import logging

from django.views import defaults
from django.shortcuts import reverse, render, redirect
from django.conf import settings

import pylast

from .models import Account


log = logging.getLogger(__name__)


def index(request):
    context = dict(
        username=request.session.get('username'),
        lastfm_api_key=settings.LASTFM_API_KEY,
        lastfm_callback_url=request.build_absolute_uri(reverse('login')),
        google_analytics_id=settings.GOOGLE_ANALYTICS_ID,
    )

    return render(request, 'index.html', context)


def login(request):
    token = request.GET.get('token')

    account = Account.from_token(token)
    if account:
        request.session['username'] = account.username
    else:
        exception = Exception("Last.fm token is invalid.")
        return defaults.permission_denied(request, exception)

    return redirect('index')


def logout(request):
    request.session.pop('username', None)

    return redirect('index')
