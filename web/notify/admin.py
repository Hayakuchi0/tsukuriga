from django.contrib import admin
from . import models


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'target', 'is_read', 'created_at')


admin.site.register(models.Notification, NotificationAdmin)
