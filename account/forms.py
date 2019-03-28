from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'description', 'profile_icon', 'profile_banner')
