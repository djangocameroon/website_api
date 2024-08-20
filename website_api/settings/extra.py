import os

from utils.main import load_documentation
from .base import BASE_DIR, TIME_ZONE, INSTALLED_APPS, MIDDLEWARE

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "exceptions.rest_exception.rest_exception_handler",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.users.pagination.CustomPagination",
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "PAGE_SIZE": 100,
    "NON_FIELD_ERRORS_KEY": "message",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Cameroon API',
    'DESCRIPTION': load_documentation('main.md'),
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': 'https://avatars.githubusercontent.com/u/142497557',
            'backgroundColor': '#FFFFFF',
            'altText': 'Django Cameroon',
            'href': 'https://djangocameroon.site',
            'style': 'margin: 0 auto; display: block; border-radius: 50%; border: 1px solid #000000;',
        }
    },
    'CONTACT': {
        'name': 'Django Cameroon',
        'url': 'https://djangocameroon.site',
        'email': 'support@djangocameroon.site',
    },
    'REDOC_SETTINGS': {
        'favicon': 'https://avatars.githubusercontent.com/u/142497557',
    },
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'POSTPROCESSING_HOOKS': [
        'utils.main.add_tag_groups'
    ],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'utils.auth.EmailOrUsernameBackend',
]

# Django extensions
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
RUNSERVER_PLUS_POLLER_RELOADER_INTERVAL = 1

# https redirect
if os.getenv("ENVIRONMENT") == "production":
    META_SITE_NAME = "Django Cameroon"
    META_USE_OG_PROPERTIES = True
    META_USE_TWITTER_PROPERTIES = True
    META_USE_TITLE_TAG = True
    META_USE_SITES = True
    META_SITE_PROTOCOL = "https"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

# AWS S3 settings
if os.getenv("ENVIRONMENT") == "production":
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = False
    WHITENOISE_MAX_AGE = 31536000

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Django Debug ToolBar settings
if os.getenv("ENVIRONMENT") == "development":
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
