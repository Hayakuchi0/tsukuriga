from django.db import models
from django.utils import timezone

import re

from markdownx.models import MarkdownxField
from core.utils import CustomModel


class Page(CustomModel):
    author = models.ForeignKey('account.User', verbose_name='筆者', null=True, on_delete=models.SET_NULL)
    title = models.CharField('タイトル', max_length=255)
    text = MarkdownxField('本文')
    slug = models.SlugField('スラッグ')
    is_published = models.BooleanField('公開する', default=True)

    def is_new(self):
        return (timezone.now() - self.created_at).days < 7

    def date_str(self):
        return self.created_at.strftime('%y/%m/%d')

    def ogp_image(self):
        imgs = re.findall('img.+src=".*', self.text)
        if imgs:
            img_src = re.findall('/.+.jpg', imgs[0])[0]
            return img_src
        return 'http://placehold.it/1200x630'

    def __str__(self):
        return self.title
