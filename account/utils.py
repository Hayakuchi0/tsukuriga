from django.contrib.auth import login
from django.core.files import File

import requests

from account.models import User, Trophy, TrophyUserRelation
from upload.utils import RequestFile


def create_and_set_trophy(user, **trophy_option):
    trophy = Trophy.objects.create(**trophy_option)
    TrophyUserRelation.objects.create(user=user, trophy=trophy)


class ImportUserException(Exception):
    pass


class ImportUser:
    instance = None
    url = 'https://altwug.net/api/v1/export/user/'

    def __init__(self, username, password):
        if User.objects.filter(username=username).exists():
            raise ImportUserException('同じユーザー名がこのサイトで既に使用されています')

        response = requests.post(self.url, {'username': username, 'password': password}).json()
        if response['is_success']:
            self._user = response.pop('user')
            self._trophies = self._user.pop('trophies')
            self._password = password
        else:
            raise ImportUserException('Altwug上にユーザーが存在しないか、パスワードが一致しませんでした')

    def login(self, request):
        login(request, self.instance, backend='django.contrib.auth.backends.ModelBackend')

    def create_user(self):
        profile_icon = RequestFile(self._user.pop('profile_icon_url'))
        profile_icon.download_file()

        profile_banner = RequestFile(self._user.pop('profile_banner_url'))
        profile_banner.download_file()

        with profile_icon.open() as icon_file, profile_banner.open() as banner_file:
            self.instance = User.objects.create_user(
                **self._user,
                password=self._password,
                profile_icon=File(icon_file),
                profile_banner=File(banner_file),
            )
            del self._password

    def create_trophies(self):
        for trophy_json in self._trophies:
            trophy_obj = Trophy.objects.filter(title=trophy_json['title'])

            if trophy_obj.exists():
                TrophyUserRelation.objects.create(user=self.instance, trophy=trophy_obj.first())
            else:
                file = RequestFile(trophy_json.pop('file_url'))
                file.download_file()
                with file.open() as f:
                    create_and_set_trophy(self.instance, file=File(f), **trophy_json)
