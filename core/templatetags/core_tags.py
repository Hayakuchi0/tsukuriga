import re

from django import template
from django.core.handlers.wsgi import WSGIRequest

from core.utils import created_at2str

register = template.Library()


@register.filter
def dt2str(arg):
    if arg:
        return created_at2str(arg)


@register.filter
def default_if_blank(arg, default):
    if arg == '':
        return default
    else:
        return arg


@register.filter
def show_if(arg, condition):
    if condition:
        return arg
    else:
        return ''


@register.filter
def show_if_not(arg, condition):
    if not condition:
        return arg
    else:
        return ''


@register.filter
def to_absolute_path(path: str, request: WSGIRequest):
    if path.strip()[:4] == 'http':
        return path
    scheme = 'https' if request.is_secure() else 'http'
    return scheme + '://' + request.get_host() + path


@register.filter
def activate_url(text):
    result = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', text)
    result = re.sub(r'(\A|\s)#(\S+)', r'<a href="/search?q=%23\2">#\2</a>', result)
    result = re.sub(r'(\A|\s)@(\S+)', r'<a href="/u/\2">@\2</a>', result)
    return result
