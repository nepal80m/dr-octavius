import os

import requests
from django.core.management.base import BaseCommand
from core.models import CoreConfig
from django.conf import settings

BASE_URL = settings.POCHITA_BASE_URL
USERNAME = settings.POCHITA_USERNAME
PASSWORD = settings.POCHITA_PASSWORD


class Command(BaseCommand):
    help = "Login and get a Auth Token for node server."

    def handle(self, *args, **options):
        try:
            res = requests.post(
                BASE_URL + "users/login/",
                data={
                    "username": USERNAME,
                    "password": PASSWORD,
                },
            )
            result = res.json()
            token = result["token"]
        except Exception as e:
            print(e)
            self.stdout.write("Error while getting pochita auth token.")
            return
        if CoreConfig.objects.filter(app="core", key="pochita_token").first() is None:
            CoreConfig.objects.create(app="core", key="pochita_token", value=token)
            self.stdout.write("Pochita Auth Token created!")
        else:
            CoreConfig.objects.filter(app="core", key="pochita_token").update(
                value=token
            )
        self.stdout.write("Pochita Auth Token updated!")
