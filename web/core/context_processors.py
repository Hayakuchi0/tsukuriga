import re
import urllib.parse

from django.conf import settings


def query_resolver(request):
    """paginationと検索クエリなど他パラメータとの競合を解決する"""
    queries = '?'
    for k, v in dict(request.GET).items():
        if not k == 'page':
            queries += f'{k}={urllib.parse.quote(v[0])}&'
    return {'queries': queries}


def user_agent_detect(request):
    ua = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META.keys() else ''
    return {
        'is_ios': len(re.findall('(iphone|ipad|ipod)', ua, re.I)) > 0
    }


def common(request):
    return {
        'DEBUG': settings.DEBUG,
        **query_resolver(request),
        **user_agent_detect(request)
    }
