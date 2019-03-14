def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'twitter':
        user.name = user.get_full_name()
        user.profile_icon_url = response.get('profile_image_url_https')
        user.profile_banner_url = response.get('profile_banner_url')
        user.description = response.get('description')
        user.save()
