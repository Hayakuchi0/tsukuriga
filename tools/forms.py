from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    name = forms.CharField(label='名前', widget=forms.TextInput(attrs={'placeholder': '名無し'}))
    text = forms.CharField(label='本文', widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'なんか書いてみてください'}))

    class Meta:
        model = Post
        fields = ('name', 'text')


class GIFEncodingForm(forms.Form):
    fps = forms.IntegerField(min_value=1)
    text = forms.CharField()
