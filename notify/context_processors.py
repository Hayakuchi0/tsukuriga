def notification(request):
    has_new = False
    if request.user.is_authenticated:
        # target=Noneはメール連投対策のために削除せず、除外することで対応する
        not_reads = request.user.received_notifications.filter(is_read=False)
        has_new = bool([n for n in not_reads if n.target])
    return {'has_new_notification': has_new}
