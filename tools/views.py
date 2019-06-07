from django.views.generic import CreateView
from django.shortcuts import redirect

from ajax.utils import get_ip
from .forms import PostForm
from .models import Post


class Chat(CreateView):
    template_name = 'chat/index.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.ip = get_ip(self.request)
        post.save()
        return redirect('/chat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('created_at')[:20]
        return context
