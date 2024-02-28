from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from celery.schedules import crontab

import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-px3ui_z*auwe6txjktx3s54xgstc**_m59&8q@)_9-r60vtd7n'

DEBUG = True

ALLOWED_HOSTS = eval(os.getenv("ALLOWED_HOSTS"))
CSRF_TRUSTED_ORIGINS = eval(os.getenv("CSRF_TRUSTED_ORIGINS"))

# Application definition
INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'poll.apps.PollConfig',
    'accounts.apps.AccountsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'accounts.middlewares.JWTAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middlewares.JWTAuthenticationMiddleware'
]

ROOT_URLCONF = 'lunch_app.urls'

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

WSGI_APPLICATION = 'lunch_app.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER':os.environ.get("DB_USER"),
        'PASSWORD':os.environ.get("DB_PASSWORD"),
        'PORT':os.environ.get("DB_PORT")
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONTEXT = {
    "basic_url":os.environ.get("BASIC_URL")
}


CELERY_TIMEZONE = 'Asia/Kolkata'


CELERY_BEAT_SCHEDULE = {
    'run-at-18-12': {
    'task': 'poll.tasks.create_scheduled_poll',
    'schedule': crontab(minute=18, hour=18, day_of_week='0-4'),  # Run at 6:12 PM from Sunday to Thursday
    },
}
