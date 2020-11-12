release: python project/manage.py makemigrations --no-input
release: python project/manage.py migrate --no-input

web: gunicorn --pythonpath . core.wsgi