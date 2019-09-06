import base64

from django.views.generic import CreateView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http.response import JsonResponse

from moviepy.editor import ImageSequenceClip

from ajax.utils import get_ip, get_anonymous_name
from upload.utils import get_tempfile
from .forms import PostForm, GIFEncodingForm, GIFTweetForm
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


@require_POST
@csrf_exempt
def para_encoding(request):
    form = GIFEncodingForm(request.POST)
    if form.is_valid():
        frames_base64 = form.cleaned_data['text'].split('@')
        temp_file_list = []

        for frame in frames_base64:
            file = ContentFile(base64.b64decode(frame))
            temp_file = get_tempfile('.png', file)
            temp_file_list.append(temp_file)

        clip = ImageSequenceClip(temp_file_list, fps=form.cleaned_data['fps'])
        gif_path = get_tempfile('.gif')
        clip.write_gif(gif_path)

        with open(gif_path, 'rb') as f:
            encoded_string = base64.b64encode(f.read())

    return JsonResponse({'base64': encoded_string.decode('utf-8')})


@require_GET
def para_authentication(request):
    return JsonResponse({
        'loginPath': '/login/twitter/?next=/para/callback',
        'isAuthenticated': request.user.is_authenticated and request.user.has_twitter_auth
    })


def para_callback(request):
    return render(request, 'para/callback.html')


@require_POST
@csrf_exempt
@login_required
def para_tweet(request):
    form = GIFTweetForm(request.POST)
    if form.is_valid():
        file = ContentFile(base64.b64decode(form.cleaned_data['media']))
        media_path = get_tempfile('.gif', file)
        with open(media_path, 'rb') as f:
            request.user.api.PostUpdate(form.cleaned_data['text'], media=f)
        return JsonResponse({'isTweeted': True})
    return JsonResponse({'isTweeted': False})
