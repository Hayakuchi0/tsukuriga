from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(label='本文', widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Post
        fields = ('name', 'text')
