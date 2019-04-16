from django.db import models
from django.utils import timezone

from notify.models import Notification
from core.utils import created_at2str, CustomModel


anonymous_names = [
    '匿名ライオン',
    '匿名ウサギ',
    '匿名トラ',
    '匿名ヘビ',
    '匿名キツネ',
    '匿名ワニ',
    '匿名サル',
    '匿名バク',
    '匿名ラクダ',
    '匿名ペンギン',
    '匿名ムササビ',
]


class Comment(models.Model):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    text = models.TextField('本文', max_length=200)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    @property
    def name(self):
        if self.is_anonymous:
            index = int(self.user.username.encode()[-1]) % len(anonymous_names)
            return anonymous_names[index]
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

    def json(self):
        return {
            'id': self.id,
            'user': self.user.json(),
            'name': self.name,
            'username': self.username,
            'profile_icon_url': self.profile_icon_url,
            'is_anonymous': self.is_anonymous,
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
        index = int(self.ip.replace('.', '')[-1]) % len(anonymous_names)
        return anonymous_names[index]


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


class DirectMessage(CustomModel):
    poster = models.ForeignKey('account.User', verbose_name='送り主', on_delete=models.CASCADE)
    receiver = models.ForeignKey('account.User', verbose_name='受取先', on_delete=models.CASCADE)
    message = models.TextField('DM本文', default='', max_length=300)
    is_anonymous = models.BooleanKey('DMを匿名にする', default=False)

    def json(self):
        return {
            'poster_name': self.poster.name(),
            'receiver': self.receiver.json(),
            'message': self.message,
            'createdAt': created_at2str(self.created_at)
        }

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.user == self.video.user:
            Notification.objects.create(recipient=self.receiver, sender=self.poster, target=self)
