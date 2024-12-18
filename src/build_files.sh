#!/bin/bash
# Install Python
apt-get update
apt-get install -y python3 python3-pip

# get the latest pip
python3.12 -m pip install --upgrade pip

# Set up the Python environment and install dependencies without caching
pip3 install --no-cache-dir -r requirements.txt

# Run your build commands
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput


