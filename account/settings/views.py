from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from ..forms import UserProfileForm, DeleteUserForm


@login_required
def edit_profile(request):
    form = UserProfileForm(initial={'profile_icon': None, 'profile_banner': None}, instance=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, '保存されました')
            return redirect(f'/u/{request.user.username}')

    return render(request, 'settings/edit.html', {'form': form, 'modal_form': DeleteUserForm()})


@require_POST
@login_required
def delete(request):
    form = DeleteUserForm(request.POST)

    if form.is_valid():
        if form.cleaned_data['username'] == request.user.username:
            request.user.delete()
            messages.success(request, '削除しました')
            return redirect(f'/')

    messages.error(request, '送信した値が不正です')
    return redirect(f'/settings/edit')
