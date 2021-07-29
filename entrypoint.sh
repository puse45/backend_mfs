#!/bin/sh
if "$DATABASE" = "mfs_africa_db"
then
    echo "Waiting for postgres..."
    echo "Host: $SQL_HOST Port: $SQL_PORT"
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py createcachetable
python manage.py shell -c "
from django.contrib.auth import get_user_model;
try:
  get_user_model().objects.filter(email='admin@admin.com').exists() or get_user_model().objects.create_superuser(username='admin',email='admin@admin.com',password='admin')
except Exception as e:
  print(e)
  "
exec "$@"
