from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from upload.models import Video
from upload.forms import VideoProfileForm
from .forms import ThumbnailForm


def top(request):
    videos = Video.objects.all().order_by('-profile__created_at')
    return render(request, 'core/top.html', {'videos': videos})


def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'core/watch.html', {'video': video})


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

    return render(request, 'core/edit.html', {'video': video, 'form': form})


@login_required
def edit_thumbnail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if not video.user == request.user:
        return HttpResponseBadRequest('ユーザー情報が投稿者と一致しません')

    form = ThumbnailForm()
    if request.method == 'POST':
        form = ThumbnailForm(request.POST)

        if form.is_valid():
            video.data.update_thumbnail(t=form.cleaned_data['time'])
            messages.success(request, '変更されました')
            return redirect(f'/watch/{video.slug}')

    return render(request, 'core/edit-thumbnail.html', {'video': video, 'form': form})
