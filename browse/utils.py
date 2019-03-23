from upload.models import Video


def safe_videos():
    return Video.objects.filter(is_active=True, profile__isnull=False, data__isnull=False)
