from django import forms
from .models import Video


class VideoFileUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('file', )
