from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'description', 'profile_icon', 'profile_banner')


class DeleteUserForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'ユーザー名を入力', 'v-model': 'deleteInput'}))
