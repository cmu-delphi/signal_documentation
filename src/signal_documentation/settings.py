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

import sentry_sdk
# Sentry init and config:
# - If you want to use Sentry, specify the DSN via the env var of `SENTRY_DSN`.
# - Useful defaults for a development environment are set below. They can be
#   changed by modifying env vars.
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), RedisIntegration(max_data_size=0)],
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', 1.0)),
        profiles_sample_rate=float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', 1.0)),
        environment=str(os.environ.get('SENTRY_ENVIRONMENT', 'development')),
        debug=str(os.environ.get('SENTRY_DEBUG', 'True')),
        attach_stacktrace=str(os.environ.get('SENTRY_ATTACH_STACKTRACE', 'True'))
    )


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

CSRF_TRUSTED_ORIGINS: list[str] = os.environ.get('CSRF_TRUSTED_ORIGINS').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []  # type: ignore

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
    'rest_framework',
    'drf_spectacular',
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


PAGE_SIZE = os.environ.get('PAGE_SIZE', 10)


# Django REST framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": os.environ.get('PAGE_SIZE', PAGE_SIZE),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

}


# DRF Spectacular settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    'TITLE': 'Signal Documentation',
    'DESCRIPTION': 'Signal Documentation API',
    'VERSION': '1.0.0',
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_REQUEST": True,
    'SERVE_PUBLIC': True,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'list',
        'filter': True,
        'tagsSorter': 'alpha',
    },
    'SERVE_INCLUDE_SCHEMA': False,
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
