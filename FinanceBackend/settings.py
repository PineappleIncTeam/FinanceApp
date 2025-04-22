import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "api.apps.ApiConfig",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "drf_yasg",
    "whitenoise.runserver_nostatic",
    "django_filters",
    "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "FinanceBackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "FinanceBackend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PG_NAME"),
        "USER": os.getenv("PG_USER"),
        "PASSWORD": os.getenv("PG_PASSWORD"),
        "HOST": os.getenv("PG_HOST"),
        "PORT": os.getenv("PG_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "api.validators.MaximumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "api.validators.EnglishLettersSymbolsPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles/admin"),
    os.path.join(BASE_DIR, "staticfiles/rest_framework"),
    os.path.join(BASE_DIR, "staticfiles/drf_spectacular_sidecar/swagger-ui-dist"),
    os.path.join(BASE_DIR, "staticfiles/drf_spectacular_sidecar/redoc"),
]
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.CustomTokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Freenance API",
    "DESCRIPTION": "DEV ENV SWAGGER",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'")

CSP_IMG_SRC = ("'self'", "data:")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOWED_ORIGINS = [
    "https://freenance.store",
    "https://dev.freenance.store",
    "http://localhost",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = [
    "freenance.store",
    "dev.freenance.store",
    "127.0.0.1",
    "localhost",
    "freenance-backend-service-dev.finance-dev.svc.cluster.local",

]

CORS_ORIGIN_WHITELIST = [
    "https://freenance.store",
    "https://dev.freenance.store",
    "http://localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://freenance.store",
    "https://dev.freenance.store" "http://localhost",
]

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DOMAIN = os.getenv("DOMAIN", "127.0.0.1:8000")

SITE_NAME = "Freenance App"

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "changePassword/?uid={uid}&token={token}",
    "USERNAME_RESET_CONFIRM_URL": "api/v1/username/reset/confirm/?uid={uid}&token={token}",
    "ACTIVATION_URL": "activate/?uid={uid}&token={token}",
    "SEND_ACTIVATION_EMAIL": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SERIALIZERS": {
        "user_create_password_retype": "api.serializers.CustomUserCreateSerializer",
        "token_create": "api.serializers.CustomTokenCreateSerializer",
    },
    "EMAIL": {"activation": "api.email.ActivationEmail"},
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGIN_REDIRECT_URL = "/"

WHITENOISE_AUTOREFRESH = True

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

LOG_FILE_NAME = "freenance.log" if DEBUG else "/var/log/freenance.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{asctime} {name} {levelname} {module} {message}",
            "style": "{",
        },
        "file": {
            "format": "{asctime} {name} {levelname} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "console",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": LOG_FILE_NAME,
            "backupCount": 0,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    },
}

MAX_OPERATIONS_COUNT = 5
DEFAULT_DATE_FORMAT_STR = "%Y-%m-%d"
DEFAULT_MONTH_FORMAT_STR = "%Y-%m"

redis_address = os.getenv("REDIS_ADR")

CELERY_BROKER_URL = f'redis://{redis_address}:6379/1'
CELERY_RESULT_BACKEND = f'redis://{redis_address}:6379/2'
CELERY_TASK_DEFAULT_QUEUE = 'celery'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{redis_address}:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
