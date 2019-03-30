from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import User
from .forms import UserProfileForm, DeleteUserForm
from upload.models import Video
from core.utils import AltPaginationListView


class CustomLogoutView(LogoutView):
    next_page = '/'

    def get_next_page(self):
        messages.success(self.request, 'ログアウトしました')
        return super().get_next_page()


class Profile(AltPaginationListView):
    template_name = 'users/profile.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        return Video.objects.filter(user__username=self.kwargs['username']).order_by('-published_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['account'] = get_object_or_404(User, username=self.kwargs['username'])
        return context


profile = Profile.as_view()


@login_required
def edit_profile(request):
    form = UserProfileForm({'name': request.user.name, 'description': request.user.description})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, '保存されました')
            return redirect(f'/u/{request.user.username}')

    return render(request, 'users/edit.html', {'form': form, 'modal_form': DeleteUserForm()})


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
    return redirect(f'/account/edit')
