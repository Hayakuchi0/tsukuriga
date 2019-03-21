from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest

from .models import Video


def users_video_required(view):
    def wrapper(request, slug, *args, **kwargs):
        video = get_object_or_404(Video, slug=slug)
        if not video.user == request.user:
            return HttpResponseBadRequest('ユーザー情報が投稿者と一致しません')
        request.video = video
        return view(request, slug, *args, **kwargs)

    return wrapper
