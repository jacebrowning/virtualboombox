import pytest
from expecter import expect


def describe_login():

    def with_missing_token(client):
        response = client.get("/login/")

        expect(response.status_code) == 403

    @pytest.mark.xfail  # TODO: this requires Last.fm key to test
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


def describe_playback():

    def is_initially_playing(client):
        response = client.get("/")

        expect(response).contains_html("Pause Playback")
