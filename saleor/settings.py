import ast
import os
from datetime import timedelta
from pytimeparse import parse
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages
from configs.configs import _SECRET_KEY, DB_NAME, DB_USER, DB_PWD, DB_HOST, \
    DB_PORT, _DEBUG, JWT_EXPIRATION, JWT_REFRESH_EXPIRATION


def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


DEBUG = get_bool_from_env("DEBUG", True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _DEBUG

# Register
ALLOW_PASSWORDLESS_REGISTRATION = True
REGISTER_MUTATION_FIELDS = 'email'

ALLOWED_HOSTS = ['127.0.0.1','104.155.209.114','35.201.139.78','localhost','saleor-mirror.default.svc.cluster.local']
ALLOWED_CIDR_NETS = ['10.0.0.0/8']

_DEFAULT_CLIENT_HOSTS = ALLOWED_HOSTS
# ALLOWED_CLIENT_HOSTS = os.environ.get("ALLOWED_CLIENT_HOSTS")

ALLOWED_CLIENT_HOSTS = _DEFAULT_CLIENT_HOSTS
if not ALLOWED_CLIENT_HOSTS:
    if DEBUG:
        ALLOWED_CLIENT_HOSTS = _DEFAULT_CLIENT_HOSTS
    else:
        raise ImproperlyConfigured(
            "ALLOWED_CLIENT_HOSTS environment variable must be set when DEBUG=False."
        )

INTERNAL_IPS = get_list(os.environ.get("INTERNAL_IPS", "127.0.0.1"))

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'django_cleanup',
    'social_django',
    "graphene_django",
    'graphql_playground',
    'background_task',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'graphql_auth',  # Django-GraphQL-Auth must be installed
]

LOCAL_APPS = [
    'apps.common',
    'apps.userprofile',
    'apps.user'
]

AUTH_USER_MODEL = 'user.CustomUser'

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # JWT
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'saleor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',  # JWT
    'graphql_auth.backends.GraphQLAuthBackend'
)

WSGI_APPLICATION = 'saleor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    },
    # 'default': {'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #           'ENGINE': 'django.db.backends.sqlite3'},

}

# ==============GQL=====================

GRAPHENE = {
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    "SCHEMA": "saleor.schema.schema",
    "SCHEMA_OUTPUT": './schema.graphql',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',  # JWT
    ],
}

ALLOWED_GRAPHQL_ORIGINS = ['104.155.209.114', '35.201.139.78']

GRAPHQL_JWT = {
    "JWT_ALGORITHM": "ES384",
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRE": False,
    "JWT_EXPIRATION_DELTA": JWT_EXPIRATION,
    "JWT_REFRESH_EXPIRATION_DELTA": JWT_REFRESH_EXPIRATION,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_ENCODE_HANDLER": 'saleor.es384.encode_ES384',
    "JWT_DECODE_HANDLER": 'saleor.es384.decode_ES384',
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
}

PLAYGROUND_ENABLED = True

GRAPHQL_AUTH = {
    'LOGIN_ALLOWED_FIELDS': ['email', 'username'],
    'ALLOW_PASSWORDLESS_REGISTRATION': True,
    'REGISTER_MUTATION_FIELDS': ['email'],

    'UPDATE_MUTATION_FIELDS': {'firebase_id':"String"},

}

# JWT_TTL_ACCESS = timedelta(seconds=parse(os.environ.get("JWT_TTL_ACCESS", "3560 days")))
# JWT_TTL_APP_ACCESS = timedelta(
#     seconds=parse(os.environ.get("JWT_TTL_APP_ACCESS", "5 minutes"))
# )
# JWT_TTL_REFRESH = timedelta(seconds=parse(os.environ.get("JWT_TTL_REFRESH", "30 days")))
#
# JWT_TTL_REQUEST_EMAIL_CHANGE = timedelta(
#     seconds=parse(os.environ.get("JWT_TTL_REQUEST_EMAIL_CHANGE", "1 hour")),
# )

LOGIN_URL = '/login/'

REAL_IP_ENVIRON = os.environ.get("REAL_IP_ENVIRON", "REMOTE_ADDR")
OPENTRACING_MAX_QUERY_LENGTH_LOG = 2000

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "zh-hant"
LANGUAGES = [
    ("en", "English"),
    ("zh-hant", "Traditional Chinese"),
]

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# try:
#     from saleor.local_settings import *
# except ImportError:
#     pass

LOGIN_REDIRECT_URL = 'dashboard'

# This will print email in Console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

_DEFAULT_CLIENT_HOSTS = "localhost,127.0.0.1"
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
