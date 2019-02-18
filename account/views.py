from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LogoutView

from .models import User


class CustomLogoutView(LogoutView):
    next_page = '/'


def profile(request, username):
    account = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'account': account})
