from uuid import uuid4
from pathlib import Path

from django.db import models
from django.core.files.storage import FileSystemStorage
from core.utils import CustomModel, gen_unique_slug


def default_video_slug():
    return gen_unique_slug(5, VideoProfile)


def video_upload_to(instance: 'VideoData', filename):
    return Path(instance.video.user.username) / 'videos' / instance.video.slug / f'{uuid4().hex}.mp4'


def temp_upload_to(instance, filename):
    file_extension = filename.split('.')[-1]
    return Path('temp') / f'{uuid4().hex}.{file_extension}'


def thumbnail_upload_to(instance: 'VideoData', filename):
    return Path(instance.video.user.username) / 'videos' / instance.video.slug / f'{uuid4().hex}.jpg'


class Video(models.Model):
    """
    関連モデルを統括する基礎モデル
    """
    user = models.ForeignKey('account.User', verbose_name='投稿者', on_delete=models.CASCADE)
    slug = models.CharField('動画ID', max_length=5, default=default_video_slug)


class UploadedPureVideo(CustomModel):
    """
    エンコード前の未処理ファイルが保持されるモデル
    """
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='pure')
    file = models.FileField('動画ファイル', upload_to=temp_upload_to, storage=FileSystemStorage())


class VideoProfile(CustomModel):
    """
    アップロード直後に情報が保持されるモデル
    基本的にユーザーが編集可
    """
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='profile')
    title = models.CharField('タイトル', max_length=50)
    description = models.TextField('動画説明', max_length=200)
    # channel = models.PositiveIntegerField
    # tags = models.PositiveIntegerField


class VideoData(models.Model):
    """
    エンコード後に作成され、情報が保持されるモデル
    基本的にユーザーが編集不可
    """
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='data')
    thumbnail = models.ImageField('サムネイル', upload_to=thumbnail_upload_to)
    file = models.FileField('動画ファイル', upload_to=video_upload_to)
    fps = models.PositiveIntegerField('FPS')
    duration = models.FloatField('動画時間')
