from django.views.generic import CreateView
from django.shortcuts import redirect

from ajax.utils import get_ip, get_anonymous_name
from .forms import PostForm
from .models import Post


class Chat(CreateView):
    template_name = 'chat/index.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.ip = get_ip(self.request)
        if self.request.user.is_authenticated:
            post.user = self.request.user
        post.save()
        return redirect('/chat')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            name = str(self.request.user)
        else:
            name = get_anonymous_name(get_ip(self.request))
        kwargs['initial'] = {'name': name}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = list(Post.objects.all().order_by('-created_at')[:20])[::-1]
        return context
