from upload.models import Video


def safe_videos():
    return Video.objects.filter(profile__release_type='published', profile__isnull=False, data__isnull=False)
