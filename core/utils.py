import math

import twitter
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import generic


def get_ip(request):
    # https://stackoverflow.com/questions/10382838/how-to-set-foreignkey-in-createview
    # https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = None
    return ip


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


def created_at2str(datetime_obj):
    def mf2str(division):
        return str(math.floor(division))

    elapsed = timezone.now() - datetime_obj
    if elapsed.days >= 365:
        return mf2str(elapsed.days/365) + '年前'
    elif elapsed.days >= 1:
        return mf2str(elapsed.days) + '日前'
    elif elapsed.seconds >= 60*60:
        return mf2str(elapsed.seconds/60/60) + '時間前'
    elif elapsed.seconds >= 60:
        return mf2str(elapsed.seconds/60) + '分前'
    else:
        return str(elapsed.seconds) + '秒前'


def ts2datetime(timestamp):
    return timezone.datetime.fromtimestamp(int(timestamp), tz=timezone.utc)


def get_tweet_url(tweet):
    return f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'


def search_loop(api: twitter.Api, logger=None, *args, **kwargs):
    result = []
    max_id = None
    loop_count = 0
    while True:
        loop_count += 1
        tweets = api.GetSearch(*args, **kwargs, count=100, max_id=max_id)
        if logger:
            print(f'search{loop_count}:{str(len(tweets))} tweets')
        if not tweets:
            break
        else:
            result.extend(tweets)
            max_id = tweets[-1].id
    return sorted(list(set(result)), key=lambda x: x.created_at_in_seconds)


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
