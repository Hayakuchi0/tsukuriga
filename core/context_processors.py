from django.conf import settings


def query_resolver(request):
    """paginationと検索クエリなど他パラメータとの競合を解決する"""
    queries = '?'
    for k, v in dict(request.GET).items():
        if not k == 'page':
            queries += f'{k}={v[0]}&'
    return {'queries': queries if not queries == '?' else ''}


def common(request):
    return {
        'DEBUG': settings.DEBUG,
        **query_resolver(request)
    }
