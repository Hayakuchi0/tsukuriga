from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import AccessLog
from ajax.utils import get_ip


@receiver(user_logged_in)
def create_access_log(sender, request, user, **kwargs):
    if user.is_authenticated:
        request_ip = get_ip(request)
        if not request_ip:
            return
        if hasattr(user, 'accesslog'):
            user.accesslog.ip_latest = request_ip
            user.accesslog.save()
        else:
            AccessLog.objects.create(
                user=user,
                ip_latest=request_ip,
                ip_joined=request_ip
            )
