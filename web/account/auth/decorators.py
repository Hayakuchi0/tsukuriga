from django.shortcuts import redirect
from django.contrib import messages

from ..models import AccessLog
from ajax.utils import get_ip


def account_create_limitation(view):
    def wrapper(request, *args, **kwargs):
        logs = AccessLog.objects.filter(ip_joined=get_ip(request))
        if logs.exists():
            log = logs.last()
            if not log.allows_create_account:
                messages.error(request, 'アカウントは一日に一つまでしか作成できません')
                return redirect('/account/login')
        return view(request, *args, **kwargs)

    return wrapper
