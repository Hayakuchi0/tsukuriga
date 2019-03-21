from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.files import File

from .models import Video, VideoProfile, UploadedPureVideo
from .utils import ImportFile
from .decorators import users_video_required
from .forms import VideoFileUploadForm, VideoProfileForm, VideoImportForm


def get_process(active_index):
    process = [
        {'title': '1. ファイル選択', 'is_active': False},
        {'title': '1-2. インポートURL入力', 'is_active': False},
        {'title': '2. 紹介文設定', 'is_active': False},
        {'title': '3. 完了！', 'is_active': False},
    ]
    process[active_index]['is_active'] = True
    return process


@login_required
def upload(request):
    form = VideoFileUploadForm()

    if request.method == 'POST':
        form = VideoFileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            video = Video.objects.create(user=request.user)
            pure_video = form.save(commit=False)
            pure_video.video = video
            pure_video.save()

            VideoProfile.objects.create(
                video=video,
                title=request.user.name + 'さんの作品'
            )

            return redirect(f'/upload/detail/{video.slug}')

    return render(request, 'upload/form.html', {'process': get_process(0), 'form': form})


@login_required
def import_upload(request):
    form = VideoImportForm()

    if request.method == 'POST':
        form = VideoImportForm(request.POST)

        if form.is_valid():
            imported = None
            try:
                imported = ImportFile(user=request.user, url=form.cleaned_data['url'])
                imported.download_file()
            except Exception as e:
                form.add_error('url', e.args[0])

            if imported is not None:
                video = Video.objects.create(user=request.user)
                video.type = imported.type
                video.save()

                with imported.open() as f:
                    UploadedPureVideo.objects.create(
                        video=video,
                        file=File(f)
                    )

                VideoProfile.objects.create(
                    video=video,
                    title=imported.title,
                    description=imported.description
                )

                return redirect(f'/upload/detail/{video.slug}')

    return render(request, 'upload/import.html', {'process': get_process(1), 'form': form})


@login_required
@users_video_required
def detail(request, slug):
    video = request.video
    form = VideoProfileForm(instance=video.profile)

    if request.method == 'POST':
        form = VideoProfileForm(request.POST, instance=video.profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.video = video
            profile.save()
            return redirect(f'/upload/complete/{video.slug}')

    return render(request, 'upload/profile.html', {'process': get_process(2), 'form': form})


@login_required
@users_video_required
def complete(request, slug):
    return render(request, 'upload/complete.html', {'process': get_process(3), 'video': request.video})
