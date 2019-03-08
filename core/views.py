from django.shortcuts import render, get_object_or_404
from upload.models import Video


def top(request):
    videos = Video.objects.all().order_by('-profile__created_at')
    return render(request, 'core/top.html', {'videos': videos})


def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'core/watch.html', {'video': video})
