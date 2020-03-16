"""
Django settings for esap project (production version)
"""

from esap.settings.base import *
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import production setting must remain False.
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'esap.sqlite3'),
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cie-((m#n$br$6l53yash45*2^mwuux*2u)bad5(0flx@krnj9'
