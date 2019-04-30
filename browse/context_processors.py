from .models import Channel


def channels(request):
    return {'channels': Channel.objects.all().order_by('number')}
