import os
import re
import tempfile

import requests

from django.core.files import File


def get_tempfile(suffix, file=None):
    """
    Windowsではdelete=Falseを指定したtempfileは権限エラーでアクセスできない
    https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
    :param str suffix:
    :param File file:
    :return:
    :rtype str
    """
    delete_option = not os.name == 'nt'

    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=delete_option)
    temp_file_path = temp_file.name

    if file is not None:
        with open(temp_file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    return temp_file_path


class ImportFile:
    def __init__(self, user, url):
        self.user = user
        self.url = url
        self.path = get_tempfile('.mp4')
        self.text = ''
        self.download_file()

    def open(self, mode='rb'):
        return open(self.path, mode=mode)

    def _get_download_url(self):
        altwug_matched = re.search(r'altwug\.net/watch/(?P<id>.+)/?', self.url)
        twitter_matched = re.search(r'twitter\.com/\w+/status/(?P<id>\d+)/?', self.url)
        if altwug_matched:
            return self._download_url_altwug(altwug_matched.group('id'))
        elif twitter_matched:
            return self._download_url_twitter(twitter_matched.group('id'))
        else:
            raise ValueError('不正なURLです')

    def _download_url_altwug(self, video_id):
        pass

    def _download_url_twitter(self, tweet_id):
        tweet = self.user.api.GetStatus(tweet_id)
        self.text = tweet.full_text
        if tweet.media and tweet.media[0].video_info:
            variants = tweet.media[0].video_info['variants']
            sorted_variants = sorted(variants, key=lambda x: x['bitrate'] if x['content_type'] == 'video/mp4' else 0)
            return sorted_variants[-1]['url']
        raise ValueError('動画ツイートではありません')

    def download_file(self):
        download_url = self._get_download_url()
        response = requests.get(download_url)
        with open(self.path, 'wb') as f:
            f.write(response.content)
