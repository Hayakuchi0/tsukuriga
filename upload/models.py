from uuid import uuid4
from pathlib import Path

from django.db import models
from core.utils import CustomModel, gen_unique_slug


def default_video_slug():
    return gen_unique_slug(5, Video)


def video_upload_to(instance: 'Video', filename):
    return Path(instance.user.username) / 'videos' / instance.slug / f'{uuid4().hex}.mp4'


def thumbnail_upload_to(instance: 'Video', filename):
    return Path(instance.user.username) / 'videos' / instance.slug / f'{uuid4().hex}.jpg'


class Video(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    slug = models.CharField(max_length=5, default=default_video_slug)
    file = models.FileField(upload_to=video_upload_to)
    fps = models.PositiveIntegerField()
    duration = models.FloatField()
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to)


class VideoProfile(CustomModel):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    # channel = models.PositiveIntegerField
    # tags = models.PositiveIntegerField
