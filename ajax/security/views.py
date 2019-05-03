from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from ajax.utils import json_response

from account.models import User
from upload.models import Video
from ajax.models import Comment


def hotline_user(username):
    user = get_object_or_404(User, username=username)
    # ここに通報情報書き込み処理を挿入
    return json_response({"message": "ご協力ありがとうございます。通報が完了しました。(通報対象:"+user.name+")"}, status=200)


def hotline_video(slug):
    video = get_object_or_404(Video, slug=slug)
    # ここに通報情報書き込み処理を挿入
    return json_response({"message": "ご協力ありがとうございます。通報が完了しました。(通報対象:"+video.id+")"}, status=200)


def hotline_comment(pk):
    if pk.isdecimal():
        comment = get_object_or_404(Comment, pk=pk)
        # ここに通報情報書き込み処理を挿入
        return json_response({"message": "ご協力ありがとうございます。通報が完了しました。(通報対象:"+comment.pk+")"}, status=200)
    return json_response({"message": "通報対象は数値で指定してください。"}, status=400)


@require_POST
def hotline(request, hotline_type, target):
    if not request.user.is_authenticated:
        return json_response({"message": "ログインしていないユーザーは通報できません。"}, status=400)
    result = json_response({"message": "不正な通報対象です。"}, status=400)
    if hotline_type == "user":
        result = hotline_user(target)
    elif hotline_type == "comment":
        result = hotline_comment(target)
    elif hotline_type == "video":
        result = hotline_video(target)
    return result
