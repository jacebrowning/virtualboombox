web: gunicorn virtualboombox.wsgi --log-file -
worker: python manage.py syncdata --loop --limit=250
