import json
import posixpath

from django.conf import settings


def load_settings(k, default=None):
    return getattr(settings, k, default)


def json_load(filepath, **kwargs):
    with open(filepath, **kwargs) as f:
        return json.load(f)


def load_credentials():
    access_file_path = load_settings('CONOHA_ACCESS_FILE_PATH')
    if access_file_path is None:
        return load_settings('CONOHA_TENANT_ID'), load_settings('CONOHA_ACCESS_TOKEN_ID')

    access_token = json_load(access_file_path)['access']['token']
    return access_token['tenant']['id'], access_token['id']


def get_container_and_filename(name):
    splited_name = name.split('/')
    if len(splited_name) == 1:
        return name, ''
    return splited_name[0], '/'.join(splited_name[1:])


def is_container(name):
    container, filename = get_container_and_filename(name)
    return filename == ''


def clean_name(name):
    """
    Cleans the name so that Windows style paths work
    https://github.com/jschneier/django-storages/blob/master/storages/utils.py
    """
    name = posixpath.normpath(name).replace('\\', '/')

    if name.endswith('/') and not name.endswith('/'):
        name = name + '/'

    if name == '.':
        name = ''

    return name
