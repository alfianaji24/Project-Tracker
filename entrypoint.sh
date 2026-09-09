#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, psycopg2
psycopg2.connect(
    dbname=os.environ.get('POSTGRES_DB', 'project_tracker'),
    user=os.environ.get('POSTGRES_USER', 'app'),
    password=os.environ.get('POSTGRES_PASSWORD', 'secret'),
    host=os.environ.get('POSTGRES_HOST', 'db'),
    port=os.environ.get('POSTGRES_PORT', '5432'),
)
" 2>/dev/null; do
  sleep 1
done

echo "PostgreSQL is ready."
python manage.py migrate --noinput
python manage.py seed_masters
python manage.py createsuperuser_if_none
exec "$@"
