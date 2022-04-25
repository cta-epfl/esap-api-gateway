"""
Django settings for ASYNC ESAP development. Extends the dev.py settings:

- Adds the UWS Django App
- Use the async-urls instead of the default one
- Configures Database with a separate Postgres db for Jobs
- Celery Configuration
"""

import os

from esap.settings.dev import *

DEBUG = bool(os.getenv("DEBUG", "False"))

# Add the UWS APP
INSTALLED_APPS = [
    "query.apps.MyAppConfig",
    "accounts",
    "rucio",
    "ida",
    "knox",
    "uws",
    "django.contrib.admin",
    "django.contrib.auth",
    "mozilla_django_oidc",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "django_filters",
]

# Use the
ROOT_URLCONF = "esap.urls_async"

# Database
DATABASE_ROUTERS = [
    "uws.database_router.UWSDatabaseRouter",
    "query.database_router.QueryRouter",
    "accounts.database_router.AccountsRouter",
    "ida.database_router.IdaRouter",
    "rucio.database_router.RucioRouter",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "esap_config.sqlite3"),
    },
    "accounts": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "esap_accounts_config.sqlite3"),
    },
    "ida": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "esap_ida_config.sqlite3"),
    },
    "rucio": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "esap_rucio_config.sqlite3"),
    },
    "uws": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "uws_jobs",
        "USER": "postgres",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "PORT": "5432",
    },
}

CELERY_TIMEZONE = "Europe/Amsterdam"
CELERY_USE_UTC = True
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest@localhost:5672")
