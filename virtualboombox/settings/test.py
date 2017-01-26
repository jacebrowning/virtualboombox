from .base import *


TEST = True
DEBUG = True
SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'TEST_NAME': 'virtualboombox_test',
    }
}
