from django.db.models import Count
from .models import Label


def labels(request):
    # https://docs.djangoproject.com/en/2.1/topics/db/aggregation/#order-by
    active_labels = Label.objects.filter(is_active=True)
    return {'labels': active_labels.annotate(count=Count('videoprofilelabelrelation')).order_by('-count')}
