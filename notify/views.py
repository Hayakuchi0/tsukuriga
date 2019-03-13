from django.views import generic

from .models import Notification


class NotificationListView(generic.ListView):
    template_name = 'notyf/index.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


notifications_list = NotificationListView.as_view()
