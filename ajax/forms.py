from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力(200文字まで)'}),
    )

    class Meta:
        model = Comment
        fields = ('text',)
