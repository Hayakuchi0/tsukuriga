from django.core.management.base import BaseCommand

from browse.models import Ranking
from upload.models import Video


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for ranking in Ranking.objects.all():
            ranking.delete()

        for video in Video.objects.all():
            video.calculate_rankings()
