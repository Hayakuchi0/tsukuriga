def notification(request):
    has_new = False
    if request.user.is_authenticated:
        has_new = request.user.notification_set.filter(is_read=False).exists()
    return {'has_new_notification': has_new}
