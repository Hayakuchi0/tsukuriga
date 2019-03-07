from django.shortcuts import render, redirect
from django.http.response import HttpResponseBadRequest

from .models import Video
from .forms import VideoFileUploadForm, VideoProfileForm


def get_process(active_index):
    process = [
        {'title': '①ファイル選択', 'is_active': False},
        {'title': '②紹介文設定', 'is_active': False},
        {'title': '③完了！', 'is_active': False},
    ]
    process[active_index]['is_active'] = True
    return process


def upload(request):
    form = VideoFileUploadForm()

    if request.method == 'POST':
        form = VideoFileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            video = Video.objects.create(user=request.user)
            pure_video = form.save(commit=False)
            pure_video.video = video
            pure_video.save()
            return redirect(f'/upload/detail?slug={video.slug}')

    return render(request, 'upload/form.html', {'process': get_process(0), 'form': form})


def detail(request):
    slug = request.GET.get('slug')
    try:
        video = Video.objects.get(slug=slug)
    except:
        return HttpResponseBadRequest()

    form = VideoProfileForm()
    if request.method == 'POST':
        form = VideoProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.video = video
            profile.save()
            return redirect(f'/upload/complete')

    return render(request, 'upload/profile.html', {'process': get_process(1), 'form': form})


def complete(request):
    return render(request, 'upload/complete.html', {'process': get_process(2)})
