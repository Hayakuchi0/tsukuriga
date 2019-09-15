from django.db import models
from django.utils import timezone
from core.utils import CustomModel, created_at2str


class Post(CustomModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    name = models.CharField('名前', max_length=20, default='名無し')
    text = models.TextField('本文', max_length=140)

    def created_at_str(self):
        if (timezone.now() - self.created_at).days < 3:
            return created_at2str(self.created_at)
        return '3日以上前'

    def __str__(self):
        return f'{self.text}({self.name})'
