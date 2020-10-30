#!/bin/bash

while !</dev/tcp/db/5432; do sleep 10; done;
./manage.py makemigrations
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
