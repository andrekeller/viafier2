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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'InsecureDefaultNeverUseItInProduction!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = any2bool(getenv('DJANGO_DEBUG', 'no'))

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', '*').split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'gallery',
    'inventory',
    'rollingstock',
]

MIDDLEWARE = [
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
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'viafier2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DJANGO_DATABASE_SCHEMA', 'viafier2'),
        'USER': getenv('DJANGO_DATABASE_USER', 'viafier2'),
        'PASSWORD': getenv('DJANGO_DATABASE_PASSWORD', 'viafier2'),
        'HOST': getenv('DJANGO_DATABASE_HOST', '127.0.0.1'),
        'PORT': int(getenv('DJANGO_DATABASE_PORT', '5432')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'de-ch'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = getenv('DJANGO_STATIC_ROOT', None)
STATICFILES_DIRS = (
    Path(BASE_DIR, 'static'),
)

CSRF_COOKIE_SECURE = any2bool(getenv('DJANGO_CSRF_COOKIE_SECURE', 'no'))
SESSION_COOKIE_SECURE = any2bool(getenv('DJANGO_SESSION_COOKIE_SECURE', 'no'))

MEDIA_URL = '/media/'
MEDIA_ROOT = getenv('DJANGO_MEDIA_ROOT', Path(BASE_DIR.parents[0], 'media'))

THUMBNAIL_SIZES = (
    250,
    600,
    950,
    1500,
)

INTERNAL_IPS = [
    '127.0.0.1',
]
LOCALEPATHS = [
    Path(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('en', _('English')),
    ('de', _('German')),
]
