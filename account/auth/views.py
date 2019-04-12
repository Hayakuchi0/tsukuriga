from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages

from ..models import User
from ..forms import SignUpForm, ImportUserForm
from ..utils import ImportUser, ImportUserException


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'ログインしました')
            return redirect('/')
    return render(request, 'auth/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        messages.success(self.request, 'ログインしました')
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    next_page = '/'

    def get_next_page(self):
        messages.success(self.request, 'ログアウトしました')
        return super().get_next_page()


def import_user(request):

    form = ImportUserForm()
    if request.method == 'POST':
        form = ImportUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            # 既存ユーザーにインポートする場合は重複を無視する
            if not request.user.is_authenticated and User.objects.filter(username=username).exists():
                raise ImportUserException('同じユーザー名がこのサイトで既に使用されています')

            imported = None
            try:
                imported = ImportUser(username, form.cleaned_data['password'])
            except ImportUserException as e:
                form.add_error('username', e.args[0])

            if imported is not None:
                if not request.user.is_authenticated:
                    imported.create_user()
                else:
                    imported.instance = request.user

                imported.create_trophies()
                imported.set_verification()
                imported.login(request)
                return redirect('/')

    return render(request, 'auth/import.html', {'form': form})
