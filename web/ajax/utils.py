from django.http import JsonResponse


def json_response(data, status=200, indent=2, *args, **kwargs):
    is_success = status == 200
    response_key = 'results' if is_success else 'errors'
    return JsonResponse(
        data={response_key: data, 'isSuccess': is_success},
        json_dumps_params={'indent': indent, 'ensure_ascii': False},
        status=status, *args, **kwargs
    )


def get_ip(request):
    # https://stackoverflow.com/questions/10382838/how-to-set-foreignkey-in-createview
    # https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = None
    return ip


def get_anonymous_name(seed):
    anonymous_names = [
        '匿名ライオン',
        '匿名ウサギ',
        '匿名トラ',
        '匿名ヘビ',
        '匿名キツネ',
        '匿名ワニ',
        '匿名サル',
        '匿名バク',
        '匿名ラクダ',
        '匿名ペンギン',
        '匿名ムササビ',
    ]
    index = int(seed.encode()[-1]) % len(anonymous_names)
    return anonymous_names[index]
