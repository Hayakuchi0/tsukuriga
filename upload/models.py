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
    user = models.ForeignKey('account.User', verbose_name='投稿者', on_delete=models.CASCADE)
    slug = models.CharField('動画ID', max_length=5, default=default_video_slug)
    file = models.FileField('動画ファイル', upload_to=video_upload_to)
    fps = models.PositiveIntegerField('FPS')
    duration = models.FloatField('動画時間')


class VideoProfile(CustomModel):
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='profile')
    title = models.CharField('タイトル', max_length=50)
    description = models.TextField('動画説明', max_length=200)
    thumbnail = models.ImageField('サムネイル', upload_to=thumbnail_upload_to)
    # channel = models.PositiveIntegerField
    # tags = models.PositiveIntegerField
