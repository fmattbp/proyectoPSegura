#!/bin/bash


su -c 'python3 -u manage.py makemigrations' limitado
su -c 'python3 -u manage.py migrate' limitado

su -c 'python3 -u manage.py runserver 0.0.0.0:8000' limitado
