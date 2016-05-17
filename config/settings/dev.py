from __future__ import absolute_import

from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env('SECRET_KEY', default='CHANGE ME!!!')

ALLOWED_HOSTS = []

ADMINS = (
    ('Dev Email', env('DEV_ADMIN_EMAIL', default='admin@localhost')),
)
MANAGERS = ADMINS


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# --------------------------------------------------------------------------

DATABASES = {
    'default': env.db(default='postgres://localhost/iwg_blog'),
}


# Email settings
# --------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = 'noreply@example.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MAILING_USE_CELERY = False


# Debug toolbar installation
# --------------------------------------------------------------------------

INSTALLED_APPS += (
    'debug_toolbar',
)


# Celery configurations
# http://docs.celeryproject.org/en/latest/configuration.html
# --------------------------------------------------------------------------

BROKER_URL = env('BROKER_URL', default='amqp://guest@localhost//')

CELERY_ALWAYS_EAGER = True


# Django meta configuration
# --------------------------------------------------------------------------

META_SITE_PROTOCOL = 'http'


# New Relic configurations
# --------------------------------------------------------------------------

NEWRELIC_DJANGO_ACTIVE = False
NEWRELIC_AVAILABILITY_TEST_ACTIVE = False


# Thumbnails configuration
# --------------------------------------------------------------------------

THUMBNAIL_DEBUG = True
