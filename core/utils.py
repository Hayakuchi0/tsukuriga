import math

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import generic
from django.conf import settings

from maintenance_mode.backends import AbstractStateBackend
from maintenance_mode.io import read_file, write_file


class AltPaginationListView(generic.ListView):

    def paginate_queryset(self, queryset, page_size):
        # 通常のページオブジェクトを取得
        # return (paginator, page, page.object_list, page.has_other_pages())
        page = super().paginate_queryset(queryset, page_size)

        # ページの前後幅を決定
        range_rate = 2

        # 送りページの幅を決定
        prev_range = page[1].number - range_rate
        if prev_range < 1:
            prev_range = 1

        # 戻りページの幅を決定
        next_range = page[1].number + range_rate + 1
        if next_range > page[0].num_pages + 1:
            next_range = page[0].num_pages + 1

        # range_rateよりあとのページなら「...」を足す
        if page[1].number > range_rate + 1:
            page[0].prev_dots = True
        # 最終ページとの差がrange_rateより大きければ「...」を足す
        if page[0].num_pages - page[1].number > range_rate:
            page[0].next_dots = True

        # 結果をalt_page_rangeとして代入
        page[0].alt_page_range = range(prev_range, next_range)
        return page

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.context_object_name:
            context['context_type'] = self.context_object_name
        return context


def created_at2str(datetime_obj):
    def mf2str(division):
        return str(math.floor(division))

    elapsed = timezone.now() - datetime_obj
    if elapsed.days >= 365:
        return mf2str(elapsed.days / 365) + '年前'
    elif elapsed.days >= 1:
        return mf2str(elapsed.days) + '日前'
    elif elapsed.seconds >= 60 * 60:
        return mf2str(elapsed.seconds / 60 / 60) + '時間前'
    elif elapsed.seconds >= 60:
        return mf2str(elapsed.seconds / 60) + '分前'
    else:
        return str(elapsed.seconds) + '秒前'


def ts2datetime(timestamp):
    return timezone.datetime.fromtimestamp(int(timestamp), tz=timezone.utc)


def get_tweet_url(tweet):
    return f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'


def gen_unique_slug(x, obj, slug_name='slug'):
    already_ids = [getattr(i, slug_name) for i in obj.objects.all()]
    while True:
        id_str = get_random_string(x)
        if id_str not in already_ids:
            return id_str


class CustomModel(models.Model):
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        abstract = True


class LocalFileBackend(AbstractStateBackend):
    """デフォルトのLocalFileBackendの各メソッドのvalueに.strip()を追加しただけのもの"""

    def get_value(self):
        value = read_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, '0')
        if value.strip() not in ['0', '1']:
            raise ValueError('state file content value is not 0|1')
        value = bool(int(value))
        return value

    def set_value(self, value):
        value = str(int(value))
        if value.strip() not in ['0', '1']:
            raise ValueError('state file content value is not 0|1')
        write_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, value)


anonymous_names = [
    '匿名ライオン',
    '匿名ウサギ',
    '匿名トラ',
    '匿名ヘビ',
    '匿名キツネ',
    '匿名ワニ',
    '匿名サル',
    '匿名バク',
    '匿名ラクダ',
    '匿名ペンギン',
    '匿名ムササビ',
]
