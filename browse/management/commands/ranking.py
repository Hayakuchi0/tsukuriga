from django.core.management.base import BaseCommand

from browse.models import Ranking
from browse.utils import safe_videos


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for ranking in Ranking.objects.all():
            ranking.delete()

        for video in safe_videos():
            video.calculate_rankings()
