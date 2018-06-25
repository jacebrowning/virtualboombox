import logging

from django.shortcuts import reverse, render, redirect
from django.conf import settings
from django.contrib import messages

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
    if request.method == 'POST':
        username = request.POST.get('username')
        request.session['username'] = username
        return redirect('index')

    token = request.GET.get('token')
    if token:
        account = Account.from_token(token)
        if account:
            request.session['username'] = account.username
            return redirect('index')
        else:
            messages.warning(
                request,
                "Sorry, we were unable to fetch your username from Last.fm",
            )

    return render(request, 'login.html')


def logout(request):
    request.session.pop('username', None)

    return redirect('index')
