import os
import traceback
from multiprocessing import Process

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munikis.settings')
django.setup()

from upload.models import UploadedPureVideo


def encode(i):
    v = UploadedPureVideo.objects.get(pk=i)
    v.make()


def main():
    videos = UploadedPureVideo.objects.all().order_by('-created_at')

    for video in videos:
        if video.is_encoding:
            continue
        try:
            process = Process(target=encode, args=[video.id])
            process.start()
            process.join()
            video.delete()
        except:
            video.is_failed = True
            video.traceback = traceback.format_exc()
            video.save()


if __name__ == '__main__':
    main()
