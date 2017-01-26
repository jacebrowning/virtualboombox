import os

import dj_database_url

from .base import *


SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'virtualboombox.com']

DATABASES = {}
DATABASES['default'] = dj_database_url.config()

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
