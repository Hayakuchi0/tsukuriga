import functools
import operator

from django.db.models import Q

from .utils import safe_videos
from core.utils import AltPaginationListView


class Home(AltPaginationListView):
    template_name = 'browse/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return safe_videos().order_by('-profile__created_at')


home = Home.as_view()


class Search(AltPaginationListView):
    template_name = 'browse/search.html'
    context_object_name = 'videos'
    q = ''

    def get_queryset(self):
        self.q = self.request.GET.get('q', '')
        q_list = self.q.split(' ')

        return safe_videos().filter(
            functools.reduce(operator.and_, (Q(profile__title__contains=item) for item in q_list)) |
            functools.reduce(operator.and_, (Q(profile__description__contains=item) for item in q_list))
        ).order_by('-profile__created_at')


search = Search.as_view()
