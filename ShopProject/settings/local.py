from .base import *

DEBUG = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.parent / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

INTERNAL_IPS = [
    '127.0.0.1',
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'