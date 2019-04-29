from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import UpdateView

from .forms import VideoProfileForm
from ajax.models import Comment


class VideoProfileUpdateView(UpdateView):
    form_class = VideoProfileForm
    pk_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        return self.request.video.profile

    def form_valid(self, form):
        video = self.request.video
        form.save()
        if not video.profile.allows_anonymous_comment:
            comments = Comment.objects.filter(video=video, is_anonymous=True)
            for comment in comments:
                comment.is_anonymous = False
                comment.save()

        if not video.is_active:
            video.publish_and_save()

        messages.success(self.request, '保存されました')
        return redirect(self.get_success_url())
