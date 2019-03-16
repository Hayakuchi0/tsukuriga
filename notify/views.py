from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Notification


class NotificationListView(generic.ListView):
    template_name = 'notify/index.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


notifications_list = login_required(NotificationListView.as_view())
