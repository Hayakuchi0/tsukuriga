from django.db.models import Count
from .models import Label


def labels(request):
    # https://docs.djangoproject.com/en/2.1/topics/db/aggregation/#order-by
    return {'labels': Label.objects.annotate(count=Count('videoprofilelabelrelation')).order_by('-count')}
