from django.db import models
from django.utils import timezone

from notify.models import Notification
from core.utils import created_at2str, CustomModel
from .utils import get_anonymous_name


class Comment(models.Model):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    text = models.TextField('本文', max_length=200)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    @property
    def name(self):
        if self.is_anonymous:
            return get_anonymous_name(self.user.username)
        return self.user.name

    @property
    def username(self):
        if self.is_anonymous:
            return ""
        return self.user.username

    @property
    def profile_icon_url(self):
        if self.is_anonymous:
            return '/assets/images/default-icon.png'
        return self.user.profile_icon_url

    def json(self, user):
        is_mine = False
        if user and user.is_authenticated:
            is_mine = user.username == self.user.username
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'profile_icon_url': self.profile_icon_url,
            'is_anonymous': self.is_anonymous,
            'is_mine': is_mine,
            'text': self.text,
            'createdAt': created_at2str(self.created_at)
        }

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.user == self.video.user:
            Notification.objects.create(recipient=self.video.user, sender=self.user, target=self)


class Point(CustomModel):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', blank=True, null=True, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('IPアドレス', blank=True, null=True)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    count = models.PositiveIntegerField('ポイント')

    def json(self):
        return {
            'id': self.id,
            'user': self.user.json() if self.user else None,
            'username': self.username_display(),
            'count': self.count,
            'createdAt': created_at2str(self.created_at)
        }

    def username_display(self):
        if self.user:
            return self.user.username
        return get_anonymous_name(self.ip)


class Favorite(CustomModel):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', on_delete=models.CASCADE)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)

    def json(self):
        return {
            'id': self.id,
            'user': self.user.json(),
            'createdAt': created_at2str(self.created_at)
        }

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.user == self.video.user:
            Notification.objects.create(recipient=self.video.user, sender=self.user, target=self)
