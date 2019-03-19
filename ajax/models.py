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
            Notification.objects.create(user=self.video.user, target=self)


class Point(CustomModel):
    user = models.ForeignKey('account.User', verbose_name='ユーザー', on_delete=models.CASCADE)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    count = models.PositiveIntegerField('ポイント')

    def json(self):
        return {
            'id': self.id,
            'user': self.user.json(),
            'count': self.count,
            'createdAt': created_at2str(self.created_at)
        }
