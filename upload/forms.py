from django import forms
from .models import UploadedPureVideo


class VideoFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPureVideo
        fields = ('file', )
