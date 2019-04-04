from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[a-zA-Z0-9_]{5,20}$'
    message = '5文字以上20文字以下でa-z, A-Z, _のみ使用可能です。'
