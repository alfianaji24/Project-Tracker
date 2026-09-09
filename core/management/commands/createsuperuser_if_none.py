import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default superuser when no users exist (development only)."

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model.objects.exists():
            self.stdout.write("Users already exist, skipping.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

        user_model.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
