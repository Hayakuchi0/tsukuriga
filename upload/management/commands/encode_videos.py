from django.core.management.base import BaseCommand
from upload.models import UploadedPureVideo


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        videos = UploadedPureVideo.objects.all().order_by('-created_at')
        for video in videos:
            video.make()
