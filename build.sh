#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing requirements..."
pip install -r DKG_ATM/requirements.txt

echo "Running migrations..."
python DKG_ATM/manage.py migrate

echo "Collecting static files..."
python DKG_ATM/manage.py collectstatic --no-input

echo "Seeding default test user..."
python DKG_ATM/create_test_user.py

echo "Build complete!"
