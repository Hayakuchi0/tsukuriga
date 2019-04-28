import functools
import operator

from django.db.models import Q

from .utils import safe_videos
from .models import Ranking
from core.utils import AltPaginationListView


class Home(AltPaginationListView):
    template_name = 'browse/index.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        return safe_videos().order_by('-published_at')


home = Home.as_view()


class Search(AltPaginationListView):
    template_name = 'browse/search.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        q_list = q.split(' ')

        return safe_videos().filter(
            functools.reduce(operator.and_, (Q(profile__title__contains=item) for item in q_list)) |
            functools.reduce(operator.and_, (Q(profile__description__contains=item) for item in q_list))
        ).order_by('-published_at')


search = Search.as_view()


class RankingList(AltPaginationListView):
    template_name = 'browse/ranking.html'
    context_object_name = 'rankings'
    paginate_by = 12

    ranking_type = 'favorites'
    ranking_day = 'week'

    def get(self, request, *args, **kwargs):
        self.ranking_type = self.kwargs.get('type', self.ranking_type)
        self.ranking_day = self.kwargs.get('day', self.ranking_day)

        Ranking.raise_http404_for_sort(self.ranking_type, self.ranking_day)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Ranking.objects.filter(type=self.ranking_type, day=self.ranking_day).order_by('-point')


ranking = RankingList.as_view()
