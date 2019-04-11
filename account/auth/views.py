from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages

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
                user.set_verification()
                user.login(request)
                return redirect(f'/')

    return render(request, 'auth/import.html', {'form': form})
