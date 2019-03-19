from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from upload.models import Video
from .models import Point
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

    if form.is_valid():
        old_point = video.point_set.filter(user=request.user).first()

        if old_point:
            old_point.count += form.cleaned_data['count']
            old_point.save()

        else:
            Point.objects.create(
                video=video,
                user=request.user if request.user.is_authenticated else None,
                ip=get_ip(request),
                count=form.cleaned_data['count']
            )
        return json_response([{'message': '評価が送信されました！'}], status=200)

    return json_response(form.errors, status=400)


@require_GET
def list_points(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return json_response([p.json() for p in video.point_set.all().order_by('-created_at')], status=200)
