#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_default_superuser
python manage.py runserver 0.0.0.0:8000

