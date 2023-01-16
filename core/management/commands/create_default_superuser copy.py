import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()

USERNAME = os.environ.get("SUPERUSER_USERNAME", "admin")
PASSWORD = os.environ.get("SUPERUSER_PASSWORD", "admin_pwd")


class Command(BaseCommand):
    help = "Create first superuser."

    def handle(self, *args, **options):
        if User.objects.filter(username=USERNAME).first() is None:
            User.objects.create_superuser(username=USERNAME, password=PASSWORD)
            self.stdout.write("Superuser created!")
        else:
            self.stdout.write("Superuser already exists!")
