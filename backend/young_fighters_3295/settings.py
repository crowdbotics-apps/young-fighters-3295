"""
Django settings for young_fighters_3295 project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import io

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5q8$cahodbg4qfv2^njnqi^m^c3^4s(_2%ehq#+%lki0%ezuzi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

try:
    # Retrieve secrets from Azure Key Vault
    azure_credentials = DefaultAzureCredential()
    vault_url = env.str("AZURE_KEYVAULT_RESOURCEENDPOINT", "")
    vault_secret_name = env.str("AZURE_KEY_VAULT_SECRET_NAME", "secrets")
    client = SecretClient(vault_url=vault_url, credential=azure_credentials)
    secret = client.get_secret(vault_secret_name)
    env.read_env(io.StringIO(secret.value))
except Exception as e:
    pass

# Configuration for Azure Storage
AS_BUCKET_NAME = env.str("AS_BUCKET_NAME", "")
if AS_BUCKET_NAME:
    AZURE_ACCOUNT_NAME = AS_BUCKET_NAME
    AZURE_TOKEN_CREDENTIAL = DefaultAzureCredential()
    AS_STATIC_CONTAINER = env.str("AS_STATIC_CONTAINER", "static")
    AS_MEDIA_CONTAINER = env.str("AS_MEDIA_CONTAINER", "media")
    AZURE_URL_EXPIRATION_SECS = env.int("AZURE_URL_EXPIRATION_SECS", 3600)
    DEFAULT_FILE_STORAGE = "young_fighters_3295.storage_backends.AzureMediaStorage"
    STATICFILES_STORAGE = "young_fighters_3295.storage_backends.AzureStaticStorage"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
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

ROOT_URLCONF = 'young_fighters_3295.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'young_fighters_3295.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

import environ
env = environ.Env()
ALLOWED_HOSTS = ['*']
SITE_ID = 1
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

if env.str("DATABASE_URL", default=None):
    DATABASES = {
        'default': env.db()
    }

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOCAL_APPS = [
    'home',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]
INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

# allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = None
LOGIN_REDIRECT_URL = '/'

if DEBUG:
    # output email to console instead of sending
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = env.str("SENDGRID_USERNAME", "")
EMAIL_HOST_PASSWORD = env.str("SENDGRID_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
