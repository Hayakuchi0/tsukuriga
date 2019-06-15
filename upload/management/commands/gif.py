from django.core.management.base import BaseCommand

from upload.models import VideoData


class Command(BaseCommand):
    def handle(self, *args, **options):
        for video in VideoData.objects.filter(gif__isnull=True, duration__gte=3):
            video.update_gif()
