import re
import html

from django import template
from django.contrib.sites.models import Site

from bulma.templatetags.bulma_tags import is_input

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
def to_absolute_path(path: str, is_secure=True):
    current_site = Site.objects.get_current()
    if not path.startswith('/'):
        return path
    path = '' if path == '/' else path
    scheme = 'https' if is_secure else 'http'
    return scheme + '://' + current_site.domain + path


@register.filter
def activate_url(text):
    if not text:
        return text
    result = html.escape(text)
    result = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', result)
    result = re.sub(r'(\A|\s)#(\S+)', r'<a href="/search?q=%23\2">#\2</a>', result)
    result = re.sub(r'(\A|\s)@(\S+)', r'<a href="/u/\2">@\2</a>', result)
    result = result.replace('\n', '<br>')
    return result


@register.filter
def is_username_field(field):
    return is_input and field.id_for_label == 'id_username'


@register.filter
def to_tight_count(count):
    result = ''
    for i in str(int(count)):
        if result == '':
            result += i
        else:
            result += '0'
    return result


@register.filter
def to_attr_list(l: list, attr) -> list:
    return [getattr(i, attr) for i in l]
