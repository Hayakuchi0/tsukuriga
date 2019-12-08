from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    name = forms.CharField(label='名前', widget=forms.TextInput(attrs={'placeholder': '名無し'}))
    text = forms.CharField(
        label='本文',
        widget=forms.Textarea(
            attrs={'rows': 6, 'placeholder': 'なんか書いてみてください。提案/不具合報告はテンプレートもあります↓'}
        ),
        help_text='<a data-action="insert-template" data-template-id="suggestion" href="#suggestion">提案用テンプレート</a>'
                  ' / '
                  '<a data-action="insert-template" data-template-id="issue" href="#issue">不具合報告用テンプレート</a>'
    )
    ua = forms.CharField(
        label='動作環境', widget=forms.TextInput(attrs={'readonly': True}),
        help_text="* 他のユーザーには見えません",
    )

    class Meta:
        model = Post
        fields = ('name', 'text', 'ua')


class GIFEncodingForm(forms.Form):
    fps = forms.IntegerField(min_value=1)
    text = forms.CharField()


class GIFTweetForm(forms.Form):
    text = forms.CharField(max_length=100, required=False)
    media = forms.CharField()
