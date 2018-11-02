"""
Django settings for viafier2 project.
"""

from os import getenv
from django.utils.translation import gettext_lazy as _
from pathlib import Path


def any2bool(obj):
    """
    returns a boolean based on a string.

    str('0'), str('false') and str('no') evaluate to False, others
    evaluate to bool(obj)
    """
    if isinstance(obj, str) and obj.lower() in ['0', 'false', 'no']:
        return False
    else:
        return bool(obj)


BASE_DIR = Path(__file__).parents[1]

SECRET_KEY = getenv('DJANGO_SECRETKEY', 'InsecureDefaultNeverUseItInProduction!')
DEBUG = any2bool(getenv('DJANGO_DEBUG', 'no'))
ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', '*').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'taggit',
    'taggit_selectize',
    # viafier2
    'common',
    'gallery',
    'inventory',
    'rollingstock',
]

MIDDLEWARE = [
    #'django.middleware.locale.LocaleMiddleware',
    #'common.middleware.ForceLanguageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

ROOT_URLCONF = 'viafier2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'viafier2.wsgi.application'

if any2bool(getenv('DJANGO_DATABASE_SSL', 'true')):
    DATABASE_OPTIONS = {
        'sslmode': 'require',
    }
else:
    DATABASE_OPTIONS = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DJANGO_DATABASE_SCHEMA', 'viafier2'),
        'USER': getenv('DJANGO_DATABASE_USER', 'viafier2'),
        'PASSWORD': getenv('DJANGO_DATABASE_PASSWORD', 'viafier2'),
        'HOST': getenv('DJANGO_DATABASE_HOST', '127.0.0.1'),
        'PORT': int(getenv('DJANGO_DATABASE_PORT', '5432')),
        'OPTIONS': DATABASE_OPTIONS,
    }
}

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

LANGUAGE_CODE = 'de-ch'
TIME_ZONE = 'UTC'
CURRENCY = 'CHF'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    Path(BASE_DIR, 'locale'),
]
LANGUAGES = [
    ('de', _('German')),
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

S3_BACKENDS = getenv('S3_BACKENDS', 'media static').split()

if S3_BACKENDS:
    AWS_ACCESS_KEY_ID = getenv('S3_ACCESSKEY')
    AWS_SECRET_ACCESS_KEY = getenv('S3_SECRETKEY')
    AWS_S3_ENDPOINT_URL = "https://{}".format(getenv('S3_ENDPOINT', 'objects.cloudscale.ch'))
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = getenv('S3_CUSTOMDOMAIN')
    MEDIASTORAGE_BUCKET = getenv('S3_MEDIA_BUCKET', 'media')
    STATICSTORAGE_BUCKET = getenv('S3_STATIC_BUCKET', 'static')

MEDIA_URL = '/media/'
THUMBNAIL_SIZES = (
    300,
    600,
    1200,
    1800,
)
if 'media' in S3_BACKENDS:
    DEFAULT_FILE_STORAGE = 'viafier2.s3storages.MediaStorage'
else:
    MEDIA_ROOT = getenv('DJANGO_MEDIA_ROOT', Path(BASE_DIR.parents[0], 'media'))

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    Path(BASE_DIR, 'static'),
)
if 'static' in S3_BACKENDS:
    STATICFILES_STORAGE = 'viafier2.s3storages.StaticStorage'
else:
    STATIC_ROOT = getenv('DJANGO_STATIC_ROOT', Path(BASE_DIR.parents[0], 'static'))


CSRF_COOKIE_SECURE = any2bool(getenv('DJANGO_CSRF_COOKIE_SECURE', 'no'))
SESSION_COOKIE_SECURE = any2bool(getenv('DJANGO_SESSION_COOKIE_SECURE', 'no'))

TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'


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
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_debug_false': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_debug_false'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        }
    },
}
