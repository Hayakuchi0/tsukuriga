from .base import *
import pymysql
from django.db.backends.mysql.schema import DatabaseSchemaEditor

# 開発環境でのストレージやメールの動作検証用に.envで変更可能
DEBUG = env('DEBUG', default=False)

WEBPACK_LOADER['DEFAULT']['CACHE'] = not DEBUG

ADMINS = [('admin', env('ADMIN_MAIL', default='admin@example.com'))]
SERVER_EMAIL = 'admin@tsukuriga.net'

if not DEBUG:
    # 設定参考
    # https://qiita.com/shirakiya/items/71861325b2c8988979a2
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django',
            'USER': 'root',
            'PASSWORD': env('MYSQL_ROOT_PASSWORD'),
            'HOST': 'db',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY',
            },
        }
    }
    pymysql.install_as_MySQLdb()
    DatabaseSchemaEditor.sql_create_table += " ROW_FORMAT=DYNAMIC"

    # 設定参考
    # https://www.monotalk.xyz/blog/Validate-security-settings-by-adding-deploy-option-to-Django-check-command/
    # security.W004
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # security.W006
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # security.W007
    SECURE_BROWSER_XSS_FILTER = True
    # security.W008
    SECURE_SSL_REDIRECT = True
    # security.W012
    SESSION_COOKIE_SECURE = True
    # security.W016, security.W017
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    # security.W019
    X_FRAME_OPTIONS = 'DENY'
    # security.W021
    SECURE_HSTS_PRELOAD = True

# django-storage-swift
DEFAULT_FILE_STORAGE = 'swift.storage.SwiftStorage'
SWIFT_AUTH_URL = 'https://identity.tyo1.conoha.io/v2.0'
SWIFT_BASE_URL = 'https://storage.tsukuriga.net'
SWIFT_AUTO_BASE_URL = False
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
