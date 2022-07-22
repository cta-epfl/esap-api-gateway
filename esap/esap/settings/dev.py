"""
Django settings for esap project for development
"""

from esap.settings.base import *

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_DEV = True
# USE_DOP457 = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
DATABASE_ROUTERS = [
    'query.database_router.QueryRouter',
    'accounts.database_router.AccountsRouter',
    'ida.database_router.IdaRouter',
    'batch.database_router.BatchRouter',
    'rucio.database_router.RucioRouter',
]

DATABASE_DIR = BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'esap_config.sqlite3'),
    },
    'accounts': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'esap_accounts_config.sqlite3'),
    },
    'ida': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'esap_ida_config.sqlite3'),
    },
    'batch': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'esap_batch_config.sqlite3'),
    },
    'rucio': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'esap_rucio_config.sqlite3'),
    },

}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# configuration settings that can be requested through the REST API
CONFIGURATION_DIR = os.path.join(BASE_DIR, 'configuration')
CONFIGURATION_FILE = 'adex'

LOGIN_REDIRECT_URL = "http://localhost:8080/esap-gui/login"
LOGOUT_REDIRECT_URL = "http://localhost:8080/esap-gui/logout"
LOGIN_REDIRECT_URL_FAILURE = "http://localhost:8080/esap-gui/error"

OIDC_RP_CLIENT_ID = ""
OIDC_RP_CLIENT_SECRET = ""
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://github.com/login/oauth/authorize"

OIDC_TOKEN_USE_BASIC_AUTH = "false"
OIDC_OP_TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
OIDC_OP_USER_ENDPOINT = "https://api.github.com/user"

# to test refresh
# OIDC_AUTHENTICATION_CALLBACK_URL = "https://localhost:8081/esap-api/oidc/callback/"

OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 36000

LOG_FILE_NAME = os.path.join("/var/log/esap/esap.log")
#LOG_FILE_NAME = os.path.join(BASE_DIR, "../logs/esap.log")
