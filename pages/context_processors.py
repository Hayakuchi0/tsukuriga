from .models import Page


def pages(request):
    try:
        submenu_message = Page.objects.get(slug='submenu').body
    except:
        submenu_message = ''

    return {
        'pages': Page.objects.filter(is_published=True).order_by('-created_at')[:5],
        'submenu_message': submenu_message
    }
