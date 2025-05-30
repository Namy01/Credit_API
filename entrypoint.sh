#!/bin/bash
set -e  # Exit if any command fails

# Wait for the DB if needed (optional with wait-for-it)

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
