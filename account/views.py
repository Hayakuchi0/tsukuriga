from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import User
from .forms import (
    SignUpForm, UserProfileForm, DeleteUserForm,
    ImportUserForm
)
from .utils import ImportUser, ImportUserException
from ajax.models import Favorite
from upload.models import Video
from core.utils import AltPaginationListView


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'ログインしました')
            return redirect('/')
    return render(request, 'users/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, 'ログインしました')
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    next_page = '/'

    def get_next_page(self):
        messages.success(self.request, 'ログアウトしました')
        return super().get_next_page()


def get_tabs(n, username):
    tabs = [
        {'href': f'/u/{username}', 'title': '投稿動画', 'is_active': False},
        {'href': f'/u/{username}/favorites', 'title': 'お気に入りリスト', 'is_active': False},
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


@login_required
def edit_profile(request):
    form = UserProfileForm(initial={'profile_icon': None, 'profile_banner': None}, instance=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, '保存されました')
            return redirect(f'/u/{request.user.username}')

    return render(request, 'users/edit.html', {'form': form, 'modal_form': DeleteUserForm()})


@require_POST
@login_required
def delete(request):
    form = DeleteUserForm(request.POST)

    if form.is_valid():
        if form.cleaned_data['username'] == request.user.username:
            request.user.delete()
            messages.success(request, '削除しました')
            return redirect(f'/')

    messages.error(request, '送信した値が不正です')
    return redirect(f'/account/edit')


def import_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = ImportUserForm()
    if request.method == 'POST':
        form = ImportUserForm(request.POST)

        if form.is_valid():
            user = None

            try:
                user = ImportUser(form.cleaned_data['username'], form.cleaned_data['password'])
            except ImportUserException as e:
                form.add_error('username', e.args[0])

            if user is not None:
                user.create_user()
                user.create_trophies()
                user.login(request)
                return redirect(f'/')

    return render(request, 'users/import.html', {'form': form})
