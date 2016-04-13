from __future__ import absolute_import

from .base import *


environ.Env.read_env()


DEBUG = False

ADMINS = env.json('ADMINS')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

SECRET_KEY = env('SECRET_KEY')


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# --------------------------------------------------------------------------

DATABASES = {
    'default': env.db(),
}


# Template
# --------------------------------------------------------------------------

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]


# --------------------------------------------------------------------------

USE_COMPRESSOR = env.bool('USE_COMPRESSOR')
USE_CLOUDFRONT = env.bool('USE_CLOUDFRONT')
USE_HTTPS = env.bool('USE_HTTPS')


# Storage configurations
# --------------------------------------------------------------------------

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_AUTO_CREATE_BUCKET = True


AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = USE_HTTPS
AWS_S3_FILE_OVERWRITE = False


if USE_CLOUDFRONT:
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    S3_URL = '//%s/' % AWS_S3_CUSTOM_DOMAIN
else:
    S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = S3_URL + 'static/'
MEDIA_URL = S3_URL + 'media/'

DEFAULT_FILE_STORAGE = 'config.settings.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'config.settings.s3utils.StaticRootS3BotoStorage'

AWS_PRELOAD_METADATA = True


# Compressor & Cloudfront settings
# --------------------------------------------------------------------------

if USE_CLOUDFRONT or USE_COMPRESSOR:
    AWS_HEADERS = {'Cache-Control': str('public, max-age=604800')}

if USE_COMPRESSOR:
    INSTALLED_APPS += ('compressor',)
    STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

    # See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
    COMPRESS_ENABLED = True

    COMPRESS_STORAGE = STATICFILES_STORAGE

    # See: http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_HASHING_METHOD
    COMPRESS_CSS_HASHING_METHOD = 'content'

    COMPRESS_CSS_FILTERS = (
        'config.settings.abs_compress.CustomCssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter'
    )

    COMPRESS_OFFLINE = True
    COMPRESS_OUTPUT_DIR = "cache"
    COMPRESS_CACHE_BACKEND = "locmem"


# Email settings
# --------------------------------------------------------------------------

EMAIL_CONFIG = env.email()
vars().update(EMAIL_CONFIG)

DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'iwg_blog '.capitalize() + '<%s>' % env('SERVER_EMAIL')


# Google analytics settings
# --------------------------------------------------------------------------

GOOGLE_ANALYTICS_PROPERTY_ID = env('GA_PROPERTY_ID', default='')
GA_ENABLED = bool(GOOGLE_ANALYTICS_PROPERTY_ID)


# Celery configurations
# http://docs.celeryproject.org/en/latest/configuration.html
# --------------------------------------------------------------------------

from kombu import Exchange, Queue

BROKER_URL = env('BROKER_URL')

CELERY_SEND_TASK_ERROR_EMAILS = True

CELERY_DEFAULT_QUEUE = 'iwg_blog-queue'
CELERY_DEFAULT_EXCHANGE = 'iwg_blog-queue'
CELERY_DEFAULT_ROUTING_KEY = 'iwg_blog-queue'
CELERY_QUEUES = (
    Queue('iwg_blog-queue', Exchange('iwg_blog-queue'), routing_key='iwg_blog-queue'),
)


# New Relic configurations
# --------------------------------------------------------------------------

# Enable/disable run newrelic python agent with django application.
NEWRELIC_DJANGO_ACTIVE = environ.bool('NEWRELIC_DJANGO_ACTIVE')

if NEWRELIC_DJANGO_ACTIVE:
    NEWRELIC_INI = environ('NEWRELIC_INI')
    NEWRELIC_ENV = environ('NEWRELIC_ENV')

# If you're going to disable availability test task, make sure you disable availability monitor test
# in synthetics tab of new relic account.
NEWRELIC_AVAILABILITY_TEST_ACTIVE = environ.bool('NEWRELIC_AVAILABILITY_TEST_ACTIVE')

if NEWRELIC_AVAILABILITY_TEST_ACTIVE:
    INSTALLED_APPS += [
        'iwg_blog.availability_monitor',
    ]
