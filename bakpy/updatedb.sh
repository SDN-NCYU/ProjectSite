#! /bin/bash
echo "inspect db"
python manage.py inspectdb

echo "inspect db > excuse/models.py"
python manage.py inspectdb > excuse/models.py

echo "makemigrations"
python manage.py makemigrations

echo "migrate"
python manage.py migrate
