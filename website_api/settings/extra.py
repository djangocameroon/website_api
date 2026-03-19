import os

from utils.main import load_documentation
from .base import BASE_DIR, DEBUG, TIME_ZONE, INSTALLED_APPS, MIDDLEWARE

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
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "resend_verification": "3/hour",
    },
    "DEFAULT_PAGINATION_CLASS": "apps.users.pagination.CustomPagination",
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "PAGE_SIZE": 100,
    "NON_FIELD_ERRORS_KEY": "message",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Cameroon API',
    'DESCRIPTION': load_documentation('main.md'),
    'EXTENSIONS_INFO': {
        'x-logo': {
            'url': 'https://avatars.githubusercontent.com/u/142497557',
            'backgroundColor': '#FFFFFF',
            'altText': 'Django Cameroon',
            'href': 'https://djangocameroon.org',
            'style': 'margin: 0 auto; display: block; border-radius: 50%; border: 1px solid #000000;',
        }
    },
    'CONTACT': {
        'name': 'Django Cameroon',
        'url': 'https://djangocameroon.org',
        'email': 'support@djangocameroon.org',
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

# ---------------------------------------------------------------------------
# Static files: always served via WhiteNoise
# ---------------------------------------------------------------------------
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MAX_AGE = 0 if DEBUG else 31536000

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------------------------------------------------
# Media files: S3/MinIO in production (DEBUG=False), local in development
# ---------------------------------------------------------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not DEBUG:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME') or None
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL') or None

    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN') or None
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL', 'public-read')
    AWS_QUERYSTRING_AUTH = os.getenv('AWS_QUERYSTRING_AUTH', 'False').lower() in ('true', '1')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    elif AWS_S3_ENDPOINT_URL:
        MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'
    else:
        MEDIA_URL = '/media/'
else:
    MEDIA_URL = '/media/'

# ---------------------------------------------------------------------------
# Redis cache — uses REDIS_URL, falls back to CELERY_BROKER_URL
# ---------------------------------------------------------------------------
REDIS_URL = os.getenv('REDIS_URL') or os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# ---------------------------------------------------------------------------
# Celery
# ---------------------------------------------------------------------------
from celery.schedules import crontab

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BEAT_SCHEDULE = {
    'send-event-reminders-daily': {
        'task': 'apps.events.tasks.send_event_reminders_task',
        'schedule': crontab(hour=9, minute=0),
        'kwargs': {'hours': 24, 'send_sms': False},
    },
    'send-monthly-events-digest': {
        'task': 'apps.events.tasks.send_monthly_digest_task',
        'schedule': crontab(day_of_month=1, hour=10, minute=0),
        'kwargs': {'days': 30, 'send_sms': False},
    },
}

# django-celery-beat (DatabaseScheduler for beat container)
INSTALLED_APPS += ['django_celery_beat']

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
