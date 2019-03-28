import re
import tempfile

import requests

from account.models import User


def get_tempfile(suffix, file=None):
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp_file_path = temp_file.name

    if file is not None:
        with open(temp_file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    return temp_file_path


class RequestFile:
    def __init__(self, url, suffix):
        self.url = url
        self.path = get_tempfile(suffix)

    def open(self, mode='rb'):
        return open(self.path, mode=mode)

    def _download_file(self, url):
        response = requests.get(url)
        with open(self.path, 'wb') as f:
            f.write(response.content)

    def download_file(self):
        self._download_file(self.url)


class ImportFile(RequestFile):
    def __init__(self, user: User, url: str):
        super().__init__(url, '.mp4')
        self.user = user
        self.title = user.name + 'さんの作品'
        self.description = ''
        self.type = 'normal'

    def _get_download_url(self):
        altwug_matched = re.search(r'altwug\.net/watch/(?P<id>.+)/?', self.url)
        twitter_matched = re.search(r'twitter\.com/\w+/status/(?P<id>\d+)/?', self.url)
        if altwug_matched:
            self.type = 'altwug'
            return self._download_url_altwug(altwug_matched.group('id'))
        elif twitter_matched:
            self.type = 'twitter'
            return self._download_url_twitter(twitter_matched.group('id'))
        else:
            raise ValueError('対応する形式のURLを入力してください')

    def _raise_for_verification(self, user_id):
        twitter_user = self.user.api.VerifyCredentials()
        if user_id is None or not twitter_user.id == user_id:
            raise ValueError('連携しているツイッターアカウントが一致しませんでした')

    def _download_url_altwug(self, video_id):
        response = requests.get(f'https://altwug.net/api/v1/export/{video_id}/').json()
        self._raise_for_verification(response['verified_id'])

        self.title = response['title']
        self.description = response['description']
        return response['download_url']

    def _download_url_twitter(self, tweet_id):
        tweet = self.user.api.GetStatus(tweet_id)
        self._raise_for_verification(tweet.user.id)

        self.description = tweet.full_text
        if tweet.media and tweet.media[0].video_info:
            variants = tweet.media[0].video_info['variants']
            sorted_variants = sorted(variants, key=lambda x: x['bitrate'] if x['content_type'] == 'video/mp4' else 0)
            return sorted_variants[-1]['url']
        raise ValueError('動画ツイートではありません')

    def download_file(self):
        url = self._get_download_url()
        self._download_file(url)
