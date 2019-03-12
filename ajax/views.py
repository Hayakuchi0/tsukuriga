from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from upload.models import Video
from .forms import CommentForm
from .utils import json_response


@require_POST
@login_required
def add_comment(request, slug):
    try:
        video = Video.objects.get(slug=slug)
    except:
        return json_response([{'message': '動画が存在しません'}], status=400)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.video = video
        comment.save()
        return json_response([{'message': 'コメントが追加されました'}], status=200)

    return json_response(form.errors, status=400)
