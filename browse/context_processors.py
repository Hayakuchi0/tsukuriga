from .models import Labels


def labels(request):
    return {'labels': Labels.objects.all().order_by('number')}
