from django import forms

from .models import Comment, Point, DirectMessage


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力(200文字まで)'}),
    )

    class Meta:
        model = Comment
        fields = ('text',)


class AddPointForm(forms.Form):
    count = forms.IntegerField(
        label='', widget=forms.NumberInput(attrs={'v-model': 'pointInput', 'readonly': True, 'style': 'display:none;'}),
        min_value=1
    )


class DirectMessageForm(forms.Form):
    is_anonymous = forms.BooleanField(label='匿名で送る', initial=False)
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'ダイレクトメッセージを入力(300文字まで)'})
    )

    class Meta:
        model = DirectMessage
        fields = ('is_anonymous', 'message')
