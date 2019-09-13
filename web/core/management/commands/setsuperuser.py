from account.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        u = User.objects.first()
        u.is_superuser = True
        u.is_staff = True
        u.save()
