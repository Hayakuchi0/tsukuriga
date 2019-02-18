from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Page


def show_page(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    if not page.is_published and not request.user.is_staff:
        raise Http404
    return render(request, 'pages/show.html', {'page': page})
