from django.shortcuts import redirect
from django.contrib import messages

from extra_views import UpdateWithInlinesView

from .models import VideoProfile
from .forms import VideoProfileForm, LabelInline
from browse.models import VideoProfileLabelRelation
from ajax.models import Comment


class VideoProfileUpdateView(UpdateWithInlinesView):
    model = VideoProfile
    form_class = VideoProfileForm
    inlines = [LabelInline]

    def post(self, request, *args, **kwargs):
        # 順番を入れ替えたとき(ラベルA, B, NoneをB, A, Noneにしたときなど)に重複のエラーが出る
        # 過去のデータを参照している？全てNULLにしておくことで回避できた
        rels = VideoProfileLabelRelation.objects.filter(profile=self.request.video.profile)
        for rel in rels:
            rel.label = None
            rel.save()
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.video.profile

    def forms_valid(self, form, inlines):
        video = self.request.video
        form.save()
        for formset in inlines:
            formset.save()

        if not video.profile.allows_anonymous_comment:
            comments = Comment.objects.filter(video=video, is_anonymous=True)
            for comment in comments:
                comment.is_anonymous = False
                comment.save()

        if not video.is_active:
            video.publish_and_save()

        messages.success(self.request, '保存されました')
        return redirect(self.get_success_url())

    def forms_invalid(self, form, inlines):
        # クラス名が書かれたようなやつが出るので、汎用的なメッセージで上書きしたい
        for formset in inlines:
            for error in formset.errors:
                if '__all__' in error.keys():
                    error['__all__'] = ['指定した値が不正です']
        return super().forms_invalid(form=form, inlines=inlines)
