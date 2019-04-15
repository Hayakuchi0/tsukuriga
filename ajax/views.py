from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q

from upload.models import Video
from account.models import User
from .models import Comment, Point, DirectMessage
from .forms import CommentForm, AddPointForm, DirectMessageForm
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


@require_POST
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user:
        comment.delete()
        return json_response([{'message': 'コメントが削除されました'}], status=200)
    return json_response([{'message': 'ユーザー情報がコメントと一致しません'}], status=400)


@require_GET
def list_comments(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return json_response([c.json() for c in video.comment_set.all().order_by('-created_at')])


@require_POST
def add_point(request, slug):
    video = get_object_or_404(Video, slug=slug)
    form = AddPointForm(request.POST)

    if form.is_valid():
        if request.user.is_authenticated:
            old_point = video.point_set.filter(user=request.user).first()
        else:
            old_point = video.point_set.filter(user__isnull=True, ip=get_ip(request)).first()

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


@require_POST
@login_required
def toggle_favorite(request, slug):
    video = get_object_or_404(Video, slug=slug)

    has_old_favorite = video.favorite_set.filter(user=request.user).exists()
    if has_old_favorite:
        old_favorite = video.favorite_set.first()
        old_favorite.delete()
        message = 'お気に入りリストから削除しました'
    else:
        video.favorite_set.create(user=request.user)
        message = 'お気に入りリストに追加しました'

    return json_response({'message': message, 'isCreated': not has_old_favorite}, status=200)


@require_GET
def list_favorites(request, slug):
    video = get_object_or_404(Video, slug=slug)
    favorites = video.favorite_set.all().order_by('-created_at')

    is_created = False
    for favorite in favorites:
        if favorite.user == request.user:
            is_created = True

    return json_response({
        'favorites': [f.json() for f in favorites],
        'isCreated': is_created
    }, status=200)


@require_POST
@login_required
def post_direct_message(request, slug):
    receiver = get_object_or_404(User, username=slug)
    if not receiver:
        return json_response({"message": "宛先のユーザーが存在しません。"}, status=404)
    form = DirectMessageForm(request.POST)
    if form.is_valid():
        dm = form.save()
        dm.receiver = receiver
        dm.poster = request.user
        dm.save()
        return json_response({"message": "メッセージを送信しました。"}, status=200)
    return json_response(form.errors, status=400)


@require_GET
def list_direct_message(requrest, slug):
    user = get_object_or_404(User, username=slug)
    messages = DirectMessage.filter(
        Q(receiver=user) |
        Q(poster=user)
    ).order_by('-created_at')
    return json_response([p.json() for p in messages], status=200)
