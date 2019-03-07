from django import forms
from .models import UploadedPureVideo, VideoProfile


class VideoFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPureVideo
        fields = ('file', )


class VideoProfileForm(forms.ModelForm):
    class Meta:
        model = VideoProfile
        fields = ('title', 'description')
