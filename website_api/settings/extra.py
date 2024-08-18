import os

from utils.main import load_documentation

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
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
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
            'style': 'margin: 0 auto; display: block;',
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
