from django.http import JsonResponse


def json_response(data, status=200, indent=2, *args, **kwargs):
    is_success = status == 200
    response_key = 'results' if is_success else 'errors'
    return JsonResponse(
        data={response_key: data, 'isSuccess': is_success},
        json_dumps_params={'indent': indent, 'ensure_ascii': False},
        status=status, *args, **kwargs
    )
