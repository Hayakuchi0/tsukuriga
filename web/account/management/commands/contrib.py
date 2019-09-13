from django.core.management.base import BaseCommand

from account.models import User


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for user in User.objects.all():
            user.calculate_contrib()
