import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")  # Default username
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@andrew.cmu.edu")  # Default email
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")  # Default password


class Command(BaseCommand):
    help = "Automatically creates a superuser"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
