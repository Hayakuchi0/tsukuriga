from django.core.files import File
from django.contrib import messages

from upload.utils import RequestFile


def save_profile(request, response, backend, user, is_new, *args, **kwargs):
    if backend.name == 'twitter' and is_new:
        user.name = response.get('name')
        user.description = response.get('description')
        user.save()

        profile_icon_url = response.get('profile_image_url_https')

        if profile_icon_url:
            profile_icon = RequestFile(profile_icon_url.replace('normal', '400x400'), '.jpg')
            profile_icon.download_file()
            with profile_icon.open() as icon_file:
                user.profile_icon = File(icon_file)
                user.save()

        profile_banner_url = response.get('profile_banner_url')

        if profile_banner_url:
            profile_banner = RequestFile(profile_banner_url, '.jpg')
            profile_banner.download_file()
            with profile_banner.open() as banner_file:
                user.profile_banner = File(banner_file)
                user.save()

    messages.success(request, 'ログインしました')
