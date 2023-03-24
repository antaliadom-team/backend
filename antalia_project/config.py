from datetime import timedelta

# настройки валидации паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 7},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# настройки rest-framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# настройки simple-jwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# настройки Djoser
DJOSER = {
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': False,
    'HIDE_USERS': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'PASSWORD_RESET_CONFIRM_EXPIRE_MINUTES': 60,
    'PASSWORD_RESET_CONFIRM_TOKEN_LENGTH': 64,
    'TOKEN_MODEL': None,
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_list': ['djoser.permissions.CurrentUserOrAdmin'],
    },
    'SERIALIZERS': {
        'user': 'api.serializers.user_serializers.UserSerializer',
        'current_user': 'api.serializers.user_serializers.UserSerializer',
        'user_create_password_retype': 'api.serializers.user_serializers.RegisterUserSerializer',
    },
}

# настройки swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'JWT [Bearer {JWT}]': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}
