"""Development settings and globals."""

import os

from .base import *

###############################################################################
# Core


DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'dev'

INSTALLED_APPS += [
    'livereload',
]

MIDDLEWARE += [
    'livereload.middleware.LiveReloadScript',
]

###############################################################################
# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'virtualboombox_dev',
    }
}

###############################################################################
# Google Analytics

GOOGLE_ANALYTICS_ID = 'localhost'
