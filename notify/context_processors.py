def notification(request):
    return {
        'has_new_notification': request.user.notification_set.filter(is_read=False).exists(),
    }
