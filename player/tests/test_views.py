# pylint: disable=unused-variable,expression-not-assigned

import pytest
from expecter import expect

from django.conf import settings


def describe_login():

    def with_missing_token(client):
        response = client.get("/login/")

        expect(response.status_code) == 403

    @pytest.mark.xfail(not settings.LASTFM_API_KEY, reason="Last.fm key unset")
    def with_invalid_token(client):
        response = client.get("/login/", {'token': "invalid"})

        expect(response.status_code) == 403


def describe_logout():

    def it_redirects(client):
        response = client.get("/logout/")

        expect(response.status_code) == 302
        expect(response['Location']) == "/"

    def it_clears_the_session(client):
        response = client.get("/logout/", follow=True)

        expect(response.status_code) == 200
        expect(response).contains_html("Share your Last.fm")
