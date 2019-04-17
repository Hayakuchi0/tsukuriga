from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import User
from ajax.models import Favorite, DirectMessage
from ajax.forms import DirectMessageForm
from upload.models import Video
from core.utils import AltPaginationListView


def get_tabs(n, username):
    tabs = [
        {'href': f'/u/{username}', 'title': '投稿動画', 'is_active': False},
        {'href': f'/u/{username}/favorites', 'title': 'お気に入りリスト', 'is_active': False},
        {'href': f'/u/{username}/direct_messages', 'title': 'ダイレクトメッセージ', 'is_active': False},
    ]
    tabs[n]['is_active'] = True
    return tabs

class AbstractProfile(AltPaginationListView):
    template_name = 'users/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        account = get_object_or_404(User, username=self.kwargs['username'])
        context['account'] = account
        context['direct_message_form'] = DirectMessageForm()
        context['tabs'] = get_tabs(self.tabs, context['account'].username)
        return context



class Profile(AbstractProfile):
    context_object_name = 'videos'
    paginate_by = 12
    tabs = 0

    def get_queryset(self):
        return Video.objects.filter(user__username=self.kwargs['username']).order_by('-published_at')


profile = Profile.as_view()


class FavoritesList(AbstractProfile):
    context_object_name = 'videos'
    paginate_by = 12
    tabs = 1

    def get_queryset(self):
        favorites = Favorite.objects.filter(user__username=self.kwargs['username']).order_by('-created_at')
        return [favorite.video for favorite in favorites]


favorites_list = FavoritesList.as_view()


class DirectMessagesList(AbstractProfile):
    context_object_name = 'direct_messages'
    paginate_by = 30
    tabs = 2

    def get_queryset(self):
        return DirectMessage.objects.filter(
            Q(receiver__username=self.kwargs['username']) |
            Q(poster__username=self.kwargs['username'])
        ).order_by('-created_at')


direct_messages_list = DirectMessagesList.as_view()
