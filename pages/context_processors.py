from .models import Page


def pages(request):
    return {'pages': Page.objects.filter(is_published=True).order_by('-created_at')[:5]}
