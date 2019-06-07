from django.db import models
from core.utils import CustomModel


class Post(CustomModel):
    name = models.CharField('名前', max_length=20)
    text = models.TextField('本文', max_length=140)

    def __str__(self):
        return f'{self.text}({self.name})'
