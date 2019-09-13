from django import forms


class ThumbnailForm(forms.Form):
    time = forms.FloatField(label='', widget=forms.NumberInput(attrs={'style': 'display: none;'}))


class DeleteVideoForm(forms.Form):
    slug = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '動画IDを入力', 'v-model': 'deleteInput'}))
