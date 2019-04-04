from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='ユーザー名(id)', help_text='先頭に@を付けてユーザーを一意に識別するためのIDです。')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'description', 'profile_icon', 'profile_banner')


class DeleteUserForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'ユーザー名を入力', 'v-model': 'deleteInput'}))


class ImportUserForm(forms.Form):
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
