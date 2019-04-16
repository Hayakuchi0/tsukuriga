from django.shortcuts import get_object_or_404
from django.models.db import Q

from ..models import User
from ajax.models import Favorite, DirectMessage
from upload.models import Video
from core.utils import AltPaginationListView


def get_tabs(n, username):
    tabs = [
        {'href': f'/u/{username}', 'title': '投稿動画', 'is_active': False},
        {'href': f'/u/{username}/favorites', 'title': 'お気に入りリスト', 'is_active': False},
        {'href': f'/u/{username}/direct_message', 'title': 'ダイレクトメッセージ', 'is_active': False},
    ]
    tabs[n]['is_active'] = True
    return tabs


class Profile(AltPaginationListView):
    template_name = 'users/profile.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        return Video.objects.filter(user__username=self.kwargs['username']).order_by('-published_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        account = get_object_or_404(User, username=self.kwargs['username'])
        context['account'] = account
        context['tabs'] = get_tabs(0, account.username)

        return context


profile = Profile.as_view()


class FavoritesList(AltPaginationListView):
    template_name = 'users/profile.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        favorites = Favorite.objects.filter(user__username=self.kwargs['username']).order_by('-created_at')
        return [favorite.video for favorite in favorites]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        account = get_object_or_404(User, username=self.kwargs['username'])
        context['account'] = account
        context['tabs'] = get_tabs(1, account.username)

        return context


favorites_list = FavoritesList.as_view()


class DirectMessagesList(AltPaginationListView):
    template_name = 'users/profile.html'
    context_object_name = 'direct_messages'
    paginate_by = 30

    def get_queryset(self):
        return DirectMessage.objects.filter(
            Q(receiver__username=self.kwargs['username']) |
            Q(poster__username=self.kwargs['username'])
        ).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        account = get_object_or_404(User, username=self.kwargs['username'])
        context['account'] = account
        context['tabs'] = get_tabs(2, account.username)
        return context


direct_messages_list = DirectMessagesList.as_view()
