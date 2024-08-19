#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run Django management commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
