from .prod import *

DEBUG = True

INSTALLED_APPS.extend([
    # django-extensions
    'django_extensions',
    # django-debug-toolbar
    'debug_toolbar',
])

# django-debug-toolbar
MIDDLEWARE += 'debug_toolbar.middleware.DebugToolbarMiddleware',

# django-debug-toolbar
INTERNAL_IPS = ['127.0.0.1']
