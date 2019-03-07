from django.shortcuts import render, get_object_or_404
from upload.models import Video


def top(request):
    return render(request, 'core/top.html')


def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'core/watch.html', {'video': video})
