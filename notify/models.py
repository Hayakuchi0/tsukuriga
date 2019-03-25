from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


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

    @property
    def mail_subject(self):
        titles = {
            'Comment': f'{self.target.user}さんがコメントしました'
        }
        return titles[self.type]

    @property
    def mail_body(self):
        content = get_template(self.component_path).render({'target': self.target})
        body = get_template('notify/mails/base.html').render({'content': content})
        return body

    def send_mail(self):
        mail = EmailMultiAlternatives(
            subject=self.mail_subject,
            to=[self.user.email]
        )
        mail.attach_alternative(self.mail_body, 'text/html')
        return mail.send()

    def save(self, *args, **kwargs):
        if not settings.DEBUG:
            self.send_mail()
        return super().save(*args, **kwargs)


"""
シンプルなメッセージを送信するモデル
class Message(models.Model):
    ...
"""
