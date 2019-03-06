from django.shortcuts import render
from .forms import VideoFileUploadForm


def get_process(active_index):
    process = [
        {'title': '①ファイル選択', 'is_active': False},
        {'title': '②紹介文設定', 'is_active': False},
        {'title': '③完了！', 'is_active': False},
    ]
    process[active_index]['is_active'] = True
    return process


def upload(request):
    process = get_process(0)
    form = VideoFileUploadForm()
    return render(request, 'upload/form.html', {'process': process, 'form': form})
