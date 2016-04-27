import environ


# Build paths inside the project like this: root(...)
env = environ.Env()

root = environ.Path(__file__) - 3
apps_root = root.path('iwg_blog')

BASE_DIR = root()


# Base configurations
# --------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# Application definition
# --------------------------------------------------------------------------

CUSTOMIZE_APPS = [
    'grappelli',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'mailing',
    'django_markdown',
    'django_select2',
    'compressor',
    'meta',
    'watson',
]

LOCAL_APPS = [
    'iwg_blog.taskapp',
    'iwg_blog.blog',
    'iwg_blog.grantee',
    'iwg_blog.attachments',
]

INSTALLED_APPS = CUSTOMIZE_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Middleware configurations
# --------------------------------------------------------------------------

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Template configurations
# --------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('iwg_blog', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'iwg_blog.context_processors.google_analytics',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


# Fixture configurations
# --------------------------------------------------------------------------

FIXTURE_DIRS = [
    root('iwg_blog', 'fixtures'),
]


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
# --------------------------------------------------------------------------

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# --------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# --------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = root('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = [
    root('iwg_blog', 'assets'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = root('media')


# Django mailing configuration
# --------------------------------------------------------------------------

MAILING_USE_CELERY = True


# Grappelli configuration
# --------------------------------------------------------------------------

GRAPPELLI_ADMIN_TITLE = 'IWG Portal'


#Django meta configuration

META_USE_OG_PROPERTIES = True
META_USE_SITES = True
META_SITE_NAME = 'IWG Portal'


# Markdown configuration
# --------------------------------------------------------------------------

MARKDOWN_SET_PATH = 'vendor/django_markdown/sets'
MARKDOWN_SET_NAME = 'custom_markdown'
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.smarty',
    'markdown.extensions.tables',
    'markdown.extensions.attr_list',
    'iwg_blog.markdown_extensions.article_content_preview',
    'iwg_blog.markdown_extensions.images_gallery',
    'iwg_blog.markdown_extensions.embedding',
    'iwg_blog.markdown_extensions.urlize',
    'iwg_blog.markdown_extensions.images_caption',
]

MARKDOWN_EXTENSION_CONFIGS = {
    'markdown.extensions.smarty': {
        'smart_angled_quotes': True
    }
}
