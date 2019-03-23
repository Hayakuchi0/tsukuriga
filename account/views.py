from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LogoutView

from .models import User
from upload.models import Video
from core.utils import AltPaginationListView


class CustomLogoutView(LogoutView):
    next_page = '/'


class Profile(AltPaginationListView):
    template_name = 'users/profile.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        return Video.objects.filter(user__username=self.kwargs['username']).order_by('-profile__created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['account'] = get_object_or_404(User, username=self.kwargs['username'])
        return context


profile = Profile.as_view()
