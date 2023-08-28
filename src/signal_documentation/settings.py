"""
Django settings for signal_documentation project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from typing import Any

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True


# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'django-insecure-qp89p*uk4)e((599s)6p%q0ra_=j41994bge%4h)o4f=@g7s4g')
else:
    SECRET_KEY: str | None = os.environ.get('SECRET_KEY')   # type: ignore
    if not SECRET_KEY:
        raise RuntimeError('Could not find a SECRET_KEY in environment')

ALLOWED_HOSTS: list[str] = os.environ.get('ALLOWED_HOSTS').split(',') if os.environ.get('ALLOWED_HOSTS') else []  # type: ignore

CORS_ALLOWED_ORIGINS: list[str] = os.environ.get('CORS_ORIGIN_WHITELIST').split(',') if os.environ.get('CORS_ORIGIN_WHITELIST') else []  # type: ignore

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True


# Application definition

DEFAULT_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS: list[str] = [
    'bootstrap5',
    'corsheaders',
    'debug_toolbar',
    'django_extensions',
    'models_extensions',
    'django_filters',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'import_export',
]

LOCAL_APPS: list[str] = [
    'base',
    'datasources',
    'signals',
]

INSTALLED_APPS: list[str] = DEFAULT_APPS + EXTERNAL_APPS + LOCAL_APPS

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INTERNAL_IPS: list[str] = [
    '127.0.0.1',
]

ROOT_URLCONF = 'signal_documentation.urls'

TEMPLATES: list[dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'signal_documentation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES: dict[str, dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', None),
        'USER': os.environ.get('MYSQL_USER', None),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', None),
        'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
        'PORT': os.environ.get('MYSQL_PORT', 3306),
    }
}

# Django chache
# https://docs.djangoproject.com/en/4.2/topics/cache/#redis
CACHES: dict[str, dict[str, str]] = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE: str = 'en-us'

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_TZ: bool = True

LOCALE_PATHS: list[str] = [os.path.join(BASE_DIR, 'locale')]

MAIN_PAGE = os.environ.get('MAIN_PAGE', '')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL: str = f'{MAIN_PAGE}/static/'
STATICFILES_DIRS: tuple[str] = (os.path.join(BASE_DIR, 'assets'),)
STATIC_ROOT: str = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL: str = f'{MAIN_PAGE}/media/'
MEDIA_ROOT: str = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


GRAPH_MODELS: dict[str, Any] = {
  'app_labels': ["datasources"],
  'group_models': True,
}
