from django.db import models
from django.utils import timezone

from notify.models import Notification
from core.utils import created_at2str, CustomModel


class Comment(models.Model):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', on_delete=models.CASCADE)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    text = models.TextField('本文', max_length=200)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def json(self):
        return {
            'id': self.id,
            'user': self.user.json(),
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
        annonymus_names = [
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
        index = int(self.ip.replace('.', '')[-1])
        return annonymus_names[index]


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
            Notification.objects.create(recipient=self.video.user, sender=self.user, target=self)
