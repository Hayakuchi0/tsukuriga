from django.http import JsonResponse


def json_response(data, status=200, indent=2, *args, **kwargs):
    is_success = status == 200
    response_key = 'result' if is_success else 'errors'
    data['isSuccess'] = is_success
    return JsonResponse(
        data={response_key: data},
        json_dumps_params={'indent': indent, 'ensure_ascii': False},
        status=status, *args, **kwargs
    )
