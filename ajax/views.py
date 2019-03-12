from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from upload.models import Video
from .models import Comment
from .forms import CommentForm
from .utils import json_response


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
    comments = Comment.objects.filter(video=video)
    return json_response([comment.json() for comment in comments])
