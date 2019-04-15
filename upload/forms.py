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
    allows_anonymous_comment = forms.BooleanField(label='匿名のコメントを許可する', required=False)

    class Meta:
        model = VideoProfile
        fields = ('title', 'description', 'allows_anonymous_comment')


class VideoImportForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'placeholder': 'https://...'}))
