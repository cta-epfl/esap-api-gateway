"""
Django settings for esap project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cie-((m#n$br$6l53yash45*2^mwuux*2u)bad5(0flx@krnj9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'query.apps.MyAppConfig',
    'staging',
    'accounts',
    'rucio',
    'ida',
    'knox',
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
]

DATABASES = {
    'awlofar': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'awlofar',
        'USER': 'AWWORLD',
        'PASSWORD': 'WORLD',
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]


ROOT_URLCONF = 'esap.urls'

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
                'django.template.context_processors.request',
            ],
        },
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
    },
]

WSGI_APPLICATION = 'esap.wsgi.application'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'query.my_pagination.CustomPagination',
    # 'PAGE_SIZE': 50
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
# https://docs.djangoproject.com/en/1.11/topics/logging/#configuring-logging
# The default configuration: https://github.com/django/django/blob/stable/1.11.x/django/utils/log.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'my_formatter': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'my_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter',
        },
        'my_file_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'my_formatter',
            'filename': 'logs/esap.log'

        },
    },
    'loggers': {
        'query': {
            'handlers': ['my_handler', 'my_file_handler', 'mail_admins'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

# Settings for mozilla_django_oidc
# use 'mozilla_django_oidc' authentication backend
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
)
OIDC_DRF_AUTH_BACKEND = 'mozilla_django_oidc.auth.OIDCAuthenticationBackend'

OIDC_RP_CLIENT_ID = os.environ['OIDC_RP_CLIENT_ID']
OIDC_RP_CLIENT_SECRET = os.environ['OIDC_RP_CLIENT_SECRET']
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = "https://iam-escape.cloud.cnaf.infn.it/jwk"
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://iam-escape.cloud.cnaf.infn.it/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://iam-escape.cloud.cnaf.infn.it/token"
OIDC_OP_USER_ENDPOINT = "https://iam-escape.cloud.cnaf.infn.it/userinfo"

OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True

LOGIN_REDIRECT_URL = "https://sdc.astron.nl/esap-gui/login"
LOGOUT_REDIRECT_URL = "https://sdc.astron.nl/esap-gui/logout"
LOGIN_REDIRECT_URL_FAILURE = "https://sdc.astron.nl/esap-gui/error"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# configuration settings that can be requested through the REST API
VERSION = "ASTRON - version 11 nov 2020"
CONFIGURATION_DIR = os.path.join(BASE_DIR, 'configuration')
CONFIGURATION_FILE = 'esap_default'
