from .base import *

DEBUG = False

WEBPACK_LOADER['DEFAULT']['CACHE'] = not DEBUG

ADMINS = [('admin', env('ADMIN_MAIL', default='admin@example.com'))]

# django-storage-swift
DEFAULT_FILE_STORAGE = 'swift.storage.SwiftStorage'
SWIFT_AUTH_URL = 'https://identity.tyo1.conoha.io/v2.0'
SWIFT_TENANT_NAME = env('SWIFT_TENANT_NAME', default='')
SWIFT_USERNAME = env('SWIFT_USERNAME', default='')
SWIFT_PASSWORD = env('SWIFT_PASSWORD', default='')
SWIFT_AUTO_CREATE_CONTAINER_PUBLIC = True
SWIFT_AUTO_CREATE_CONTAINER = True
SWIFT_CONTAINER_NAME = 'media'

# mail
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.muumuu-mail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Tsukuriga <mail@tsukuriga.net>'
