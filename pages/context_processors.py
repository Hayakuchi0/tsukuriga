from .models import Page


def pages(request):
    try:
        submenu_message = Page.objects.get(slug='submenu').body
    except:
        submenu_message = ''

    latest_pages = Page.objects.filter(is_published=True).order_by('-created_at')
    featured_pages = sorted([p for p in latest_pages if p.featured_order], key=lambda p: p.featured_order)

    return {
        'latest_pages': latest_pages[:5],
        'featured_pages': featured_pages,
        'submenu_message': submenu_message
    }
