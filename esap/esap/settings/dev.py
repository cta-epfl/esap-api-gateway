"""
Django settings for esap project for development
"""

from esap.settings.base import *

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# USE_DOP457 = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5555",
    "http://localhost:3000",
    "http://127.0.0.1:5555",
    "http://127.0.0.1:3000",
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

# Database
DATABASE_ROUTERS = [
    'query.database_router.QueryRouter',
    'accounts.database_router.AccountsRouter',
    'staging.database_router.StagingRouter',
    'ida.database_router.IdaRouter',
    'rucio.database_router.RucioRouter',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap_config.sqlite3'),
    },
    #    'query': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': os.path.join(BASE_DIR, 'esap_config.sqlite3'),
    #    },
    'accounts': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap_accounts_config.sqlite3'),
    },
    'staging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap_staging_config.sqlite3'),
    },
    'ida': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap_ida_config.sqlite3'),
    },
    'rucio': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap_rucio_config.sqlite3'),
    },

}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# configuration settings that can be requested through the REST API
CONFIGURATION_DIR = os.path.join(BASE_DIR, 'configuration')

# CONFIGURATION_FILE = 'esap_solar'
# CONFIGURATION_FILE = 'esap_config'
CONFIGURATION_FILE = 'adex'

LOGIN_REDIRECT_URL = "http://localhost:3000/esap-gui/login"
LOGOUT_REDIRECT_URL = "http://localhost:3000/esap-gui/logout"
LOGIN_REDIRECT_URL_FAILURE = "http://localhost:3000/esap-gui/error"
