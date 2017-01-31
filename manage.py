#!.venv/bin/python

import os
import sys
import warnings

from django.core.management import execute_from_command_line
import dotenv


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dotenv.read_dotenv()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'virtualboombox.settings.dev')

    execute_from_command_line(sys.argv)
