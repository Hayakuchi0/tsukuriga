from upload.models import Video


def safe_videos():
    return Video.objects.filter(profile__isnull=False, data__isnull=False)
