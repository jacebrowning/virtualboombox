"""Development settings and globals."""

import os

from .base import *


DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'dev'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'virtualboombox_dev',
    }
}

GOOGLE_ANALYTICS_ID = 'localhost'
