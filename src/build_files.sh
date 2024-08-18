#!/bin/bash

# Install Python
apt-get update
apt-get install -y python3 python3-pip

# Set up the Python environment
pip3 install -r requirements.txt

# Run your build commands
python3 manage.py collectstatic --noinput

