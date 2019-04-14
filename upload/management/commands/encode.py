import traceback
from multiprocessing import Process

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # ファイルトップでimportするとAppRegistryNotReadyエラーが出る(encode()内のimportが無視される？)
        from upload.models import UploadedPureVideo
        videos = UploadedPureVideo.objects.all().order_by('-created_at')

        for video in videos:
            if video.is_encoding:
                continue
            try:
                process = Process(target=encode, args=[video.id])
                process.start()
                process.join()
                if process.exitcode == 0:
                    video.delete()
            except:
                video.is_failed = True
                video.traceback = traceback.format_exc()
                video.save()

                if not settings.DEBUG:
                    send_mail(
                        subject='エンコード中のエラー通知',
                        message=f'{video.traceback}\nhttps://tsukuriga.net/admin/upload/uploadedpurevideo/{video.id}/change/',
                        from_email=settings.SERVER_EMAIL,
                        recipient_list=[email for name, email in settings.ADMINS]
                    )


def encode(pk):
    import django
    django.setup()
    from upload.models import UploadedPureVideo

    v = UploadedPureVideo.objects.get(pk=pk)
    v.make()
