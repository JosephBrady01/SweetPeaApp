import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create an initial superuser from env vars if it doesn't exist."

    def handle(self, *args, **options):
        if os.environ.get("CREATE_SUPERUSER", "False") != "True":
            self.stdout.write("CREATE_SUPERUSER is not True; skipping.")
            return

        username = os.environ.get("DJANGO_ADMIN_USERNAME", "admin")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "admin@sweetpea.local")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not password:
            self.stderr.write("DJANGO_ADMIN_PASSWORD not set; cannot create superuser.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' already exists; skipping.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
