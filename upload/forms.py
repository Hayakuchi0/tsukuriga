from django import forms
from .models import UploadedPureVideo, VideoProfile


class VideoFileUploadForm(forms.ModelForm):
    file = forms.FileField(
        label='動画ファイル', widget=forms.FileInput(),
        help_text='mp4,avi,gif,movの動画ファイル、100MBまで'
    )

    class Meta:
        model = UploadedPureVideo
        fields = ('file',)


class VideoProfileForm(forms.ModelForm):
    description = forms.CharField(
        label='動画説明', widget=forms.Textarea(), required=False,
        help_text='URLと@, #から始まる文字列はそれぞれリンク、ユーザーページへのリンク、ハッシュタグに置換されます'
    )
    allows_anonymous_comment = forms.BooleanField(
        label='匿名のコメントを許可する', required=False,
        help_text='拒否設定にした時点で追加されていたコメントは全て匿名設定がオフになります'
    )

    class Meta:
        model = VideoProfile
        fields = ('title', 'description', 'is_loop', 'allows_anonymous_comment')


class VideoImportForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'placeholder': 'https://...'}))
