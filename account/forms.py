from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, DirectMessage


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='ユーザー名', help_text='先頭に@を付けてユーザーを識別するためのIDです。')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'description', 'profile_icon', 'profile_banner', 'is_accept_mail')


class DeleteUserForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'ユーザー名を入力', 'v-model': 'deleteInput'}))


class ImportUserForm(forms.Form):
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())


class DirectMessageForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(
        label='匿名で送る',
        initial=False,
        required=False
    )
    text = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'ダイレクトメッセージを入力(300文字まで)'})
    )

    class Meta:
        model = DirectMessage
        fields = ('is_anonymous', 'text')
