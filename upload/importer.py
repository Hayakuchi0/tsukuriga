import re

import requests
from django.core.files import File

from .utils import RequestFile
from .models import Video, VideoProfile, UploadedPureVideo
from account.models import User


class ImportFileError(Exception):
    pass


class ImportFile(RequestFile):
    def __init__(self, user: User, url: str):
        super().__init__(url, '.mp4')
        self.user = user
        self.importer = self._get_importer()
        self.json = self.importer()
        self.video = None

        if Video.objects.filter(source_url=url).exists():
            raise ImportFileError('すでにインポート済みの動画です')

    def _get_importer(self):
        patterns = (
            (AltwugImporter, r'^https://altwug\.net/watch/(?P<id>.+)/$'),
            (TwitterImporter, r'^https://twitter\.com/\w+/status/(?P<id>\d+)$'),
        )
        for importer, pattern in patterns:
            matched = re.search(pattern, self.url)
            if matched:
                return importer(matched.group('id'), self.user)

        raise ImportFileError('対応する形式のURLを入力してください')

    def download_file(self):
        url = self.json['download_url']
        self._download_file(url)

    def create_video(self):
        video = Video.objects.create(user=self.user, type=self.json['type'], source_url=self.url)
        self.video = video

        with self.open() as f:
            UploadedPureVideo.objects.create(
                video=video,
                file=File(f)
            )

        VideoProfile.objects.create(
            video=video,
            title=self.json['title'],
            description=self.json['description']
        )


class TwitterImporter:
    def __init__(self, tweet_id, user):
        self.user = user
        self.tweet_id = tweet_id
        if not self.user.has_social_auth('twitter'):
            raise ImportFileError('ツイッター認証が必要です')

    def __call__(self):
        tweet = self.user.api.GetStatus(self.tweet_id)

        if not self.is_valid(tweet.user.id):
            raise ImportFileError('ツイートの投稿者と連携アカウントが一致しません')

        return {
            'type': 'twitter',
            'title': self.user.name + 'さんの作品',
            'description': tweet.full_text,
            'download_url': self.get_video_url(tweet)
        }

    def is_valid(self, verification_id):
        return int(self.user.extra_data['access_token']['user_id']) == verification_id

    @staticmethod
    def get_video_url(tweet):
        if tweet.media and tweet.media[0].video_info:
            variants = tweet.media[0].video_info['variants']
            sorted_variants = sorted(variants, key=lambda x: x['bitrate'] if x['content_type'] == 'video/mp4' else 0)
            return sorted_variants[-1]['url']
        raise ImportFileError('指定したツイートは動画ツイートではありません')


class AltwugImporter:
    def __init__(self, video_id, user):
        self.user = user
        self.video_id = video_id

        if not hasattr(self.user, 'altwugauth'):
            raise ImportFileError('Altwugとの接続が必要です')

    def __call__(self):
        response = requests.get(f'https://altwug.net/api/v1/export/video/{self.video_id}/').json()

        if not self.is_valid(response['verification_id']):
            raise ImportFileError('動画の投稿者と連携アカウントが一致しません')

        return {
            'type': 'altwug',
            'title': response['title'],
            'description': response['description'],
            'download_url': response['download_url'],
        }

    def is_valid(self, verification_id):
        return self.user.altwugauth.verification_id == verification_id
