from django import forms

from .models import Comment, Point


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力(200文字まで)'}),
    )

    class Meta:
        model = Comment
        fields = ('text',)


class AddPointForm(forms.ModelForm):
    count = forms.IntegerField(
        label='', widget=forms.NumberInput(attrs={'v-model': 'pointInput'}), min_value=1
    )

    class Meta:
        model = Point
        fields = ('count',)
