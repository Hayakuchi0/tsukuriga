from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings

import os
from uuid import uuid4

import twitter
from social_django.models import UserSocialAuth


def profile_image_upload_to(instance, filename):
    return os.path.join('u', instance.username, 'profile', f'{uuid4().hex}.jpg')


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    name = models.CharField('表示名', max_length=50, null=True, blank=True)
    description = models.TextField('プロフィール文', max_length=500, null=True, blank=True)

    profile_icon = models.ImageField('プロフィール画像', upload_to=profile_image_upload_to, null=True, blank=True)
    profile_banner = models.ImageField('プロフィール背景画像', upload_to=profile_image_upload_to, null=True, blank=True)

    objects = UserManager()

    @property
    def api(self):
        social_auth_obj = UserSocialAuth.objects.get(user=self)
        api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                          consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                          access_token_key=social_auth_obj.extra_data['access_token']['oauth_token'],
                          access_token_secret=social_auth_obj.extra_data['access_token']['oauth_token_secret'],
                          tweet_mode='extended')
        return api

    def json(self):
        return {
            'username': self.username,
            'name': self.name,
            'profile_icon': self.profile_icon.url
        }

    def delete(self, **kwargs):
        self.profile_icon.delete(False)
        self.profile_banner.delete(False)
        return super().delete(**kwargs)

    class Meta(object):
        app_label = 'account'
