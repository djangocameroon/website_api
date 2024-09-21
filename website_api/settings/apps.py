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
]

# ---------------------- some extra stuff ------------------------------------- #

EXTRA_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "crequest.middleware.CrequestMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

