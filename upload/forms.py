from django import forms
from .models import UploadedPureVideo, VideoProfile


class VideoFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPureVideo
        fields = ('file',)


class VideoProfileForm(forms.ModelForm):
    description = forms.CharField(
        label='動画説明', widget=forms.Textarea(), required=False,
        help_text='URLと@, #から始まる文字列はそれぞれリンク、ユーザーページへのリンク、ハッシュタグに置換されます'
    )
    can_post_anonymous_comment = forms.BooleanField(
        label='匿名の投稿を許可する',
        required=False,
        initial=True
    )

    class Meta:
        model = VideoProfile
        fields = ('title', 'description', 'can_post_anonymous_comment')


class VideoImportForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'placeholder': 'https://...'}))
