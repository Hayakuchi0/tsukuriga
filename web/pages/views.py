from django.http import Http404
from django.shortcuts import render, get_object_or_404

from core.utils import AltPaginationListView
from .models import Page


class PagesList(AltPaginationListView):
    paginate_by = 6
    template_name = 'pages/index.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return Page.objects.filter(is_published=True).order_by('-created_at')


pages_list = PagesList.as_view()


def show_page(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    if not page.is_published and not request.user.is_staff:
        raise Http404
    return render(request, 'pages/show.html', {'page': page})
