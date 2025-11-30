#!/usr/bin/env bash
# This script runs during Render's build phase.

set -o errexit  # exit on error

# Install static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput
