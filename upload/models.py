import os
import random
import mimetypes
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property
from django.utils import timezone
from moviepy.editor import VideoFileClip

from core.utils import CustomModel, gen_unique_slug


def default_video_slug():
    return gen_unique_slug(5, Video)


def video_upload_to(instance: 'VideoData', filename):
    return os.path.join(instance.video.user.username, 'videos', instance.video.slug, f'{uuid4().hex}.mp4')


def temp_upload_to(instance: 'UploadedPureVideo', filename):
    file_extension = filename.split('.')[-1]
    return os.path.join('temp', f'{instance.video.slug}-{timezone.now().strftime("%Y%m%d%H%M%S")}.{file_extension}')


def thumbnail_upload_to(instance: 'VideoData', filename):
    return os.path.join(instance.video.user.username, 'videos', instance.video.slug, f'{uuid4().hex}.jpg')


def get_temp_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, temp_upload_to(instance, filename))


class Video(models.Model):
    """
    関連モデルを統括する基礎モデル
    """
    user = models.ForeignKey('account.User', verbose_name='投稿者', on_delete=models.CASCADE)
    slug = models.CharField('動画ID', max_length=5, default=default_video_slug, editable=False)


class UploadedPureVideo(CustomModel):
    """
    エンコード前の未処理ファイルが保持されるモデル
    """
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='pure')
    file = models.FileField('動画ファイル', upload_to=temp_upload_to, storage=FileSystemStorage())

    @cached_property
    def clip(self):
        return VideoFileClip(self.file.path)

    def is_mp4(self):
        return mimetypes.guess_type(self.file.path)[0] == 'video/mp4'

    def create_thumbnail(self):
        filepath = get_temp_path(self, '.jpg')
        t = random.randint(0, int(self.clip.duration))
        self.clip.save_frame(filepath, t=t)
        return filepath

    def encode_file(self):
        if self.is_mp4():
            return self.file.path

        encoded_path = get_temp_path(self, '.mp4')
        self.clip.write_videofile(encoded_path)
        return encoded_path

    def make(self):
        thumbnail_filepath = self.create_thumbnail()
        encoded_filepath = self.encode_file()

        with open(encoded_filepath, 'rb') as file, open(thumbnail_filepath, 'rb') as thumbnail:
            VideoData.objects.create(
                video=self.video,
                thumbnail=File(thumbnail),
                file=File(file),
                fps=self.clip.fps,
                duration=self.clip.duration
            )
        self.delete()

        self.clip.close()
        os.remove(encoded_filepath)
        os.remove(thumbnail_filepath)

    def delete(self, **kwargs):
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
        return super().delete(**kwargs)


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

    def delete(self, **kwargs):
        self.file.delete(False)
        self.thumbnail.delete(False)
        return super().delete(**kwargs)
