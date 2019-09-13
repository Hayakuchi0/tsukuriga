from django.core import validators
from django.utils.deconstruct import deconstructible

username_regex = '[a-zA-Z0-9_]{5,20}'


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = f'^{username_regex}$'
    message = '5文字以上20文字以下でa-z, A-Z, _のみ使用可能です。'
