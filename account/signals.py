from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import AccessLog
from ajax.utils import get_ip


@receiver(user_logged_in)
def create_access_log(sender, request, user, **kwargs):
    if user.is_authenticated:
        if hasattr(user, 'accesslog'):
            user.accesslog.ip_latest = get_ip(request)
            user.accesslog.save()
        else:
            AccessLog.objects.create(
                user=user,
                ip_latest=get_ip(request),
                ip_joined=get_ip(request)
            )
