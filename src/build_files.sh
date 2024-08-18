#!/bin/bash

# Debugging: Print Python and Pip versions
which python
python --version
which pip
pip --version

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
