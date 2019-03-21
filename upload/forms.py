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

    class Meta:
        model = VideoProfile
        fields = ('title', 'description')


class VideoImportForm(forms.Form):
    url = forms.URLField(
        label='URL', widget=forms.URLInput(attrs={'placeholder': 'https://...'}),
        help_text="""次の形式のURLに対応しています: <br>
twitter: https://twitter.com/{screen_name}/status/{tweet_id}<br>
altwug: https://altwug.net/watch/{video_id}/<br>
""")
