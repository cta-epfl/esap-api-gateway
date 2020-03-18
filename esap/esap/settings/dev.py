"""
Django settings for esap project for development
"""

from esap.settings.base import *

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# configuration settings that can be requested through the REST API
CONFIGURATION_DIR = os.path.join(BASE_DIR, 'configuration')
CONFIGURATION_FILE = os.path.join('esap_dev')