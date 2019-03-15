from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from ajax.forms import CommentForm
from upload.models import Video
from upload.forms import VideoProfileForm
from .forms import ThumbnailForm, DeleteVideoForm


def top(request):
    videos = Video.objects.all().order_by('-profile__created_at')
    return render(request, 'core/top.html', {'videos': videos})


def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    form = CommentForm()
    return render(request, 'core/watch.html', {'video': video, 'form': form})


@login_required
def edit(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if not video.user == request.user:
        return HttpResponseBadRequest('ユーザー情報が投稿者と一致しません')

    form = VideoProfileForm(instance=video.profile)
    if request.method == 'POST':
        form = VideoProfileForm(request.POST, instance=video.profile)

        if form.is_valid():
            form.save()
            messages.success(request, '保存されました')
            return redirect(f'/watch/{video.slug}')

    return render(request, 'core/edit.html', {'video': video, 'form': form, 'modal_form': DeleteVideoForm()})


@login_required
def edit_thumbnail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if not video.user == request.user:
        return HttpResponseBadRequest('ユーザー情報が投稿者と一致しません')

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

    return render(request, 'core/edit-thumbnail.html', {'video': video, 'form': form})


@require_POST
@login_required
def delete(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if not video.user == request.user:
        return HttpResponseBadRequest('ユーザー情報が投稿者と一致しません')

    form = DeleteVideoForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['slug'] == video.slug:
            video.delete()
            messages.success(request, '削除しました')
            return redirect(f'/u/{request.user.username}')

    messages.error(request, '送信した値が不正です')
    return redirect(f'/edit/{slug}')
