from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from ajax.forms import CommentForm, AddPointForm
from upload.models import Video
from upload.forms import VideoProfileForm
from upload.decorators import users_video_required
from .forms import ThumbnailForm, DeleteVideoForm


def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    video.views_count += 1
    video.save()
    return render(request, 'core/watch.html', {'video': video, 'form': CommentForm(), 'modal_form': AddPointForm()})


@login_required
@users_video_required
def edit(request, slug):
    video = request.video
    form = VideoProfileForm(instance=video.profile)

    if request.method == 'POST':
        form = VideoProfileForm(request.POST, instance=video.profile)

        if form.is_valid():
            form.save()

            if not video.is_active:
                video.publish_and_save()

            messages.success(request, '保存されました')
            return redirect(f'/watch/{video.slug}')

    return render(request, 'core/edit.html', {'video': video, 'form': form, 'modal_form': DeleteVideoForm()})


@login_required
@users_video_required
def edit_thumbnail(request, slug):
    video = request.video
    if not video.is_encoded:
        messages.error(request, 'エンコードが完了するまでは利用できません')
        return redirect(f'/edit/{video.slug}')

    form = ThumbnailForm()

    if request.method == 'POST':
        form = ThumbnailForm(request.POST)

        if form.is_valid():
            t = form.cleaned_data['time']

            if 0 <= t <= video.data.duration:
                video.data.update_thumbnail(t=t)
                messages.success(request, '変更されました')
                return redirect(f'/watch/{video.slug}')

            messages.error(request, '指定した秒数が不正です')

    return render(request, 'core/thumbnail.html', {'video': video, 'form': form})


@require_POST
@login_required
@users_video_required
def delete(request, slug):
    video = request.video
    form = DeleteVideoForm(request.POST)

    if form.is_valid():
        if form.cleaned_data['slug'] == video.slug:
            video.delete()
            messages.success(request, '削除しました')
            return redirect(f'/u/{request.user.username}')

    messages.error(request, '送信した値が不正です')
    return redirect(f'/edit/{slug}')
