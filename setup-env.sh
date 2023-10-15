#!/bin/bash

source venv/bin/activate
cd backend
rm db.sqlite3
# create models for for creating its contenttypes
python manage.py migrate rules
# when contenttypes exist, permissions can be set
python manage.py migrate api
# run all migrations now
python manage.py migrate
python manage.py loaddata test_user
python manage.py loaddata test_firewallobjects
python manage.py loaddata test_rules
#python manage.py loaddata test_rulesetrequests
