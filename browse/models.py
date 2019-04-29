from django.db import models
from django.utils import timezone
from django.http.response import Http404

DAY_SETS = (
    (1, 'day', '24時間'),
    (7, 'week', '週間'),
    (30, 'month', '月間'),
    (-1, 'all', '全期間'),
)


def day_to_count(name):
    for count, pathname, label in DAY_SETS:
        if pathname == name:
            return count


class Ranking(models.Model):
    DAYS = tuple([
        (pathname, label) for count, pathname, label in DAY_SETS
    ])
    TYPES = (
        ('favorites', 'お気に入り順'),
    )
    point = models.IntegerField('算出ポイント', default=0)
    video = models.ForeignKey('upload.Video', verbose_name='動画', on_delete=models.CASCADE)
    day = models.CharField('期間(日)', default=1, max_length=20, choices=DAYS)
    type = models.CharField('集計タイプ', default='popular', max_length=20, choices=TYPES)

    @staticmethod
    def raise_http404_for_sort(t, d):
        type_labels = [v for v, k in Ranking.TYPES]
        day_labels = [v for v, k in Ranking.DAYS]
        if t not in type_labels or d not in day_labels:
            raise Http404

    @property
    def day_count(self):
        return day_to_count(self.day)

    @property
    def from_datetime(self):
        if self.day_count > 0:
            return timezone.now() - timezone.timedelta(self.day_count)
        raise Exception('期間の値が不正です')

    def calculate(self):
        calculator = self.get_calculator()
        self.point = calculator()

    def get_calculator(self):
        calculator_name = f'calc_{self.type}'
        if hasattr(self, calculator_name):
            return getattr(self, calculator_name)
        raise NotImplementedError(calculator_name + 'メソッドが定義されていません')

    def calc_favorites(self):
        if self.day_count == -1:
            return self.video.favorites_count
        return len(self.video.favorite_set.filter(created_at__gte=self.from_datetime))


class Channel(models.Model):
    number = models.PositiveSmallIntegerField('番号', unique=True)
    title = models.CharField('タイトル', max_length=50)
    description = models.TextField('説明')

    def __str__(self):
        return f'{self.title}({self.number}ch)'
