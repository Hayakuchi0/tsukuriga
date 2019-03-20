from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Notification(models.Model):
    user = models.ForeignKey('account.User', verbose_name='受診者', on_delete=models.CASCADE)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.IntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    @property
    def is_new(self):
        is_read = self.is_read
        self.is_read = True
        self.save()
        return not is_read

    @property
    def type(self):
        return type(self.target).__name__

    @property
    def component_path(self):
        return f'notify/components/types/{self.type}.html'

    def save(self, *args, **kwargs):
        # ここでメール送信
        return super().save(*args, **kwargs)


"""
シンプルなメッセージを送信するモデル
class Message(models.Model):
    ...
"""
