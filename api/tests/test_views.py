import pytest
from expecter import expect

from player.models import Account


def describe_root():

    def describe_GET():

        def when_anon(client):
            response = client.get("/api/")

            expect(response.status_code) == 200
            expect(response).contains_json(
                accounts="http://testserver/api/accounts/",
                songs="http://testserver/api/songs/",
                queue="http://testserver/api/queue/",
            )


def describe_accounts():

    def describe_GET():

        def when_annon(client):
            response = client.get("/api/accounts/")

            expect(response.status_code) == 200
            expect(response.json()) == []


def describe_songs():

    def describe_GET():

        def when_anon(client):
            response = client.get("/api/songs/")

            expect(response.status_code) == 200
            expect(response.json()) == []


def describe_queue():

    def describe_GET():

        def when_anon(client):
            response = client.get("/api/queue/")

            expect(response.status_code) == 405
