THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "oauth2_provider",
    "django_extensions",
]

CUSTOM_APPS = [
    "apps.users",
    "apps.events",
    "apps.blog",
]

# ---------------------- some extra stuff ------------------------------------- #

EXTRA_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "crequest.middleware.CrequestMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]



# CORS configuration
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost$",
    r"^https://\w+\.djangocameroon\.site",
    r"^https://\w+\.djangocameroon\.site:$",
    r"^https://\w+\.djangocameroon\.site:\d+$",
    r"^https://\w+\.djangocameroon\.site:\d+/$",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "https://www.djangocameroon.site",
    "https://djangocameroon.site",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost",
    "https://djangocameroon.site",
    "https://beta.djangocameroon.site",
    "https://www.djangocameroon.site",
]
