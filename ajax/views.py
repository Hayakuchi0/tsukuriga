from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from upload.models import Video
from .models import Comment
from .forms import CommentForm
from .utils import json_response


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
    comments = Comment.objects.filter(video=video).order_by('-created_at')
    return json_response([comment.json() for comment in comments])
