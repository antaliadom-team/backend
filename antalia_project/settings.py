import os

from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='django-secret-key')
DEBUG = os.getenv('DEBUG', default=False) == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='127.0.0.1').split()


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_extensions',  # shell_plus --ipython
    'drf_yasg',
    'corsheaders',
    'djoser',
    'users',
    'catalog',
    'about',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/backend_media/'
MEDIA_ROOT = BASE_DIR / 'media'
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
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    X_FRAME_OPTIONS = 'DENY'

CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_WHITELIST = os.environ.get(
    'CORS_WHITELIST', default='http://localhost'
).split()

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,
}
# Djoser
DJOSER = {
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': False,
    'HIDE_USERS': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'TOKEN_MODEL': None,
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_list': ['djoser.permissions.CurrentUserOrAdmin'],
    },
    'SERIALIZERS': {
        'user': 'api.serializers.user_serializers.UserSerializer',
        'current_user': 'api.serializers.user_serializers.UserSerializer',
        'user_create': 'api.serializers.user_serializers.RegisterUserSerializer',
    },
}

# swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'JWT [Bearer {JWT}]': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}

# В файле .env хранятся имя юзера и пароль приложения
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_REPLY_TO = 'antalyadom@telfia.com'
EMAIL_ADMIN_MESSAGE = 'Поступила заявка от {admin_full_name}.'
EMAIL_USER_MESSAGE = (
    'Здравствуйте {user_full_name}. Ваша заявка была принята в работу,'
    'скоро с вами свяжется сотрудник нашего агентства.'
)
EMAIL_HTML_MESSAGE_ADMIN = ''  # можно прикрутить HTML
EMAIL_HTML_MESSAGE_USER = ''  # можно прикрутить HTML

# Константы для моделей
EMAIL_LENGTH = 50
USER_ROLE_LENGTH = 6
PHONE_LENGTH = 14
NAMES_LENGTH = 30
LONG_NAMES_LENGTH = 100
ESTATE_TITLE_LENGTH = 200
SLUG_LENGTH = 100
LONG_SLUG_LENGTH = 255
PROPERTY_MAX_LENGTH = 50
ICON_SLUG = 100
COMMENT_LENGTH = 200
CONF_CODE_LENGTH = 32
PASSWORD_LENGTH = 128
