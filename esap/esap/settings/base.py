"""
Django settings for esap project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_DEV = False

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Setup support for proxy headers,
# this should only be used if an nginx proxy is used that forwards the headers
# https://www.nginx.com/resources/wiki/start/topics/examples/forwarded/
# https://docs.djangoproject.com/en/3.2/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = True
#SECURE_SSL_REDIRECT = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'query.apps.MyAppConfig',
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

#DATABASES = {
#    'awlofar': {
#        'ENGINE': 'django.db.backends.oracle',
#        'NAME': 'awlofar',
#        'USER': 'AWWORLD',
#        'PASSWORD': 'WORLD',
#    }
#}

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
        'rest_framework.authentication.BasicAuthentication',
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

# Ensure that the output directory for the log file exists;
# it won't be created automatically.
LOG_FILE_NAME = os.path.join(BASE_DIR, "../logs/esap.log")
os.makedirs(os.path.dirname(LOG_FILE_NAME), exist_ok=True)

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
            'filename': LOG_FILE_NAME

        },
    },
    'loggers': {
        'query': {
            'handlers': ['my_handler', 'my_file_handler', 'mail_admins'],
            'level': 'INFO',
        },
        'accounts': {
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
    #'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'accounts.my_oidc.MyOIDCAB'
)
OIDC_DRF_AUTH_BACKEND = 'mozilla_django_oidc.auth.OIDCAuthenticationBackend'

# OIDC environment variables

try:
    OIDC_RP_CLIENT_ID = os.environ['OIDC_RP_CLIENT_ID']
    OIDC_RP_CLIENT_SECRET = os.environ['OIDC_RP_CLIENT_SECRET']
    OIDC_OP_JWKS_ENDPOINT = os.environ['OIDC_OP_JWKS_ENDPOINT']
    OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ['OIDC_OP_AUTHORIZATION_ENDPOINT']
    OIDC_OP_TOKEN_ENDPOINT = os.environ['OIDC_OP_TOKEN_ENDPOINT']
    OIDC_OP_USER_ENDPOINT = os.environ['OIDC_OP_USER_ENDPOINT']

    LOGIN_REDIRECT_URL = os.environ['LOGIN_REDIRECT_URL']
    LOGOUT_REDIRECT_URL = os.environ['LOGOUT_REDIRECT_URL']
    LOGIN_REDIRECT_URL_FAILURE = os.environ['LOGIN_REDIRECT_URL_FAILURE']
except:
    # OIDC settings are not configured. ESAP will work in anonymous mode
    pass

# OIDC_AUTHENTICATION_CALLBACK_URL = "https://sdc-dev.astron.nl/esap-api/oidc/callback/"
OIDC_AUTH_REQUEST_EXTRA_PARAMS = {'audience':'rucio'}
OIDC_RP_SCOPES = "openid email profile"
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True

try:
   OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = float(os.environ['OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS'])
except:
   OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 36000

# SECURITY WARNING: keep the secret key used in production secret!
# preferably read the SECRET_KEY from the environment
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except:
    SECRET_KEY = 'cie-((m#n$br$6l53yash45*2^mwuux*2u)bad5(0flx@krnj9'

# Rucio environment variables
try:
    #RUCIO_AUTH_TOKEN = os.environ['RUCIO_AUTH_TOKEN']
    #RUCIO_AUTH_HOST = os.environ['RUCIO_AUTH_HOST']
    RUCIO_HOST = os.environ['RUCIO_HOST']

except:
    #RUCIO_AUTH_TOKEN = None
    #RUCIO_AUTH_HOST = None
    RUCIO_HOST = None


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# configuration settings that can be requested through the REST API
API_VERSION = "ESAP-API version 12 aug 2021"
CONFIGURATION_DIR = os.path.join(BASE_DIR, 'configuration')
CONFIGURATION_FILE = 'esap_default'

# location of the YAML configuration files.
# currently next to the (default) 'sqlite3' files, but can be moved later.
CONFIGURATION_DATA_DIR = os.path.join(BASE_DIR)

# Customizing type of auto-created primary keys
# New in Django 3.2: https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
