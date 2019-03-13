from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    user = models.ForeignKey('account.User', verbose_name='受診者', on_delete=models.CASCADE)
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)

    @property
    def text(self):
        # targetの型から文章を生成
        text = ''
        return text

    def save(self, *args, **kwargs):
        # ここでメール送信
        return super().save(*args, **kwargs)


"""
シンプルなメッセージを送信するモデル
class Message(models.Model):
    ...
"""
