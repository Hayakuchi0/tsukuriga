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

from .validators import FileValidator, video_file_validator
from .utils import get_tempfile
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

    def is_encoded(self):
        return VideoData.objects.filter(video=self).exists()

    def delete(self, **kwargs):
        if hasattr(self, 'profile'):
            self.profile.delete()
        if hasattr(self, 'data'):
            self.data.delete()
        return super().delete(**kwargs)


class UploadedPureVideo(CustomModel):
    """
    エンコード前の未処理ファイルが保持されるモデル
    """
    video = models.OneToOneField(Video, verbose_name='動画', on_delete=models.CASCADE, related_name='pure')

    file_validator = FileValidator(allowed_extensions=['mp4'], max_size=100 * 1024 * 1024)
    file = models.FileField('動画ファイル', upload_to=temp_upload_to, storage=FileSystemStorage(),
                            validators=[file_validator, video_file_validator])

    is_encoding = models.BooleanField('エンコード開始済み', default=False)
    is_failed = models.BooleanField('エンコード失敗', default=False)
    traceback = models.TextField('トレースバック', blank=True, null=True)

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
        self.is_encoding = True
        self.save()

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

        self.clip.close()
        os.remove(encoded_filepath)
        os.remove(thumbnail_filepath)

        self.delete()

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

    def update_thumbnail(self, t):
        temp_file_path = get_tempfile('.mp4', self.file)
        clip = VideoFileClip(temp_file_path)

        next_thumbnail_path = get_tempfile('.jpg')
        clip.save_frame(next_thumbnail_path, t=t)
        clip.close()

        self.thumbnail.delete(False)
        with open(next_thumbnail_path, 'rb') as f:
            self.thumbnail = File(f)
            self.save()

    def duration_str(self):
        hour = int((self.duration / 3600))
        minute = int((self.duration % 3600) / 60)
        second = int((self.duration % 3600) % 60)

        if hour == 0:
            hour = ''
        else:
            hour = str(hour) + ':'

        result = hour + '%02d:%02d' % (minute, second)
        return result

    def delete(self, **kwargs):
        self.file.delete(False)
        self.thumbnail.delete(False)
        return super().delete(**kwargs)
