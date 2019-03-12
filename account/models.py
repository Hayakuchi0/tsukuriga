from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings

import twitter

from social_django.models import UserSocialAuth


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    name = models.CharField('表示名', max_length=50, null=True, blank=True)
    profile_icon_url = models.URLField('プロフィール画像URL', null=True, blank=True)

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
            'profile_icon': self.profile_icon_url
        }

    def profile_icon_url_medium(self):
        if self.profile_icon_url:
            return self.profile_icon_url.replace('normal', '200x200')

    def profile_icon_url_large(self):
        if self.profile_icon_url:
            return self.profile_icon_url.replace('normal', '400x400')

    class Meta(object):
        app_label = 'account'
