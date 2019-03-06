from django.shortcuts import render


def get_process(active_index):
    process = [
        {'title': 'ファイル選択', 'is_active': False},
        {'title': '紹介文設定', 'is_active': False},
        {'title': '完了！', 'is_active': False},
    ]
    process[active_index]['is_active'] = True
    return process


def upload(request):
    process = get_process(0)
    return render(request, 'upload/form.html', {'process': process})
