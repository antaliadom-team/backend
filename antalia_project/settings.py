import os
from pathlib import Path

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from antalia_project.config import *
from antalia_project.constants import *

DEBUG = os.getenv('DEBUG', default=False) == 'True'

sentry_sdk.init(
    environment='production' if not DEBUG else 'development',
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='django-secret-key')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='127.0.0.1').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_prometheus',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'djoser',
    'django_filters',
    'users',
    'catalog',
    'about',
    'api',
    'core',
    'django_cleanup',
]

if DEBUG:
    INSTALLED_APPS += ['django_extensions', 'drf_yasg']  # shell_plus --ipython

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'antalia_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

WSGI_APPLICATION = 'antalia_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', default=BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'backend_media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'backend_static'

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_ALLOW_ALL = False
    # https://dev.to/ashiqursuperfly/all-things-security-dockerizing-django-for-deploying-anywhere-5eo2
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = (
        os.environ.get('CSRF_COOKIE_SECURE', default=False) == 'True'
    )
    SESSION_COOKIE_SECURE = (
        os.environ.get('SESSION_COOKIE_SECURE', default=False) == 'True'
    )

    X_FRAME_OPTIONS = 'DENY'

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_WHITELIST = os.environ.get(
    'CORS_WHITELIST', default='http://localhost'
).split()

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# В файле .env хранятся имя юзера и пароль приложения
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', default='smtp.zeptomail.com')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = os.environ.get('EMAIL_PORT', default=587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_REPLY_TO = os.environ.get('EMAIL_REPLY_TO', default='noreply@telfia.com')
DEFAULT_FROM_EMAIL = EMAIL_REPLY_TO

# Celery Broker settings
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', default='redis://localhost:6379/0'
)
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', default='redis://localhost:6379/0'
)
