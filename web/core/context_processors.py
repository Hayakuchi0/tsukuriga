import urllib.parse

from django.conf import settings


def query_resolver(request):
    """paginationと検索クエリなど他パラメータとの競合を解決する"""
    queries = '?'
    for k, v in dict(request.GET).items():
        if not k == 'page':
            queries += f'{k}={urllib.parse.quote(v[0])}&'
    return {'queries': queries}


def common(request):
    return {
        'DEBUG': settings.DEBUG,
        **query_resolver(request)
    }
