def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'twitter':
        user.name = user.get_full_name()
        user.profile_icon_url = response.get('profile_image_url_https')
        user.save()
