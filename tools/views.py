import base64

from django.views.generic import CreateView
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http.response import JsonResponse

from moviepy.editor import ImageSequenceClip

from ajax.utils import get_ip, get_anonymous_name
from upload.utils import get_tempfile
from .forms import PostForm, GIFEncodingForm
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
def gif_encoding(request):
    form = GIFEncodingForm(request.POST)
    if form.is_valid():
        frames_base64 = form.cleaned_data['text'].split('@')
        temp_file_list = []

        for frame in frames_base64:
            file = ContentFile(base64.b64decode(frame))
            temp_file = get_tempfile('.png', file)
            temp_file_list.append(temp_file)

        clip = ImageSequenceClip(temp_file_list, fps=form.cleaned_data['fps'])
        result_path = get_tempfile('.gif')
        clip.write_gif(result_path)
        print(result_path)

    return JsonResponse({'result': 'success'})
