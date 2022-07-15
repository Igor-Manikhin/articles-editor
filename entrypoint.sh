#!/bin/bash

python manage.py migrate
python manage.py loaddata init_db_dump.json
python manage.py runserver 0.0.0.0:8000
