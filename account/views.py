from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User
from .forms import UserProfileForm
from upload.models import Video
from core.utils import AltPaginationListView


class CustomLogoutView(LogoutView):
    next_page = '/'


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
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, '保存されました')
            return redirect(f'/u/{request.user.username}')

    return render(request, 'users/edit.html', {'form': form})
