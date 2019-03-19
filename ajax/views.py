from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from upload.models import Video
from .forms import CommentForm, AddPointForm
from .utils import json_response, get_ip


def login_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return json_response([{'message': 'ログインが必要です'}], status=401)
        return view(request, *args, **kwargs)

    return wrapper


@require_POST
@login_required
def add_comment(request, slug):
    video = get_object_or_404(Video, slug=slug)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.video = video
        comment.save()
        return json_response([{'message': 'コメントが追加されました'}], status=200)

    return json_response(form.errors, status=400)


@require_GET
def list_comments(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return json_response([c.json() for c in video.comment_set.all().order_by('-created_at')])


@require_POST
@login_required
def add_point(request, slug):
    video = get_object_or_404(Video, slug=slug)

    form = AddPointForm(request.POST)
    if form.is_valid() and not request.user == video.user:
        point = form.save(commit=False)
        if request.user.is_authenticated:
            point.user = request.user
        else:
            point.ip = get_ip(request)
        point.video = video
        point.save()
        return json_response([{'message': '評価が送信されました！'}], status=200)

    return json_response(form.errors, status=400)


@require_GET
def list_points(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return json_response([p.json() for p in video.point_set.all().order_by('-created_at')], status=200)
