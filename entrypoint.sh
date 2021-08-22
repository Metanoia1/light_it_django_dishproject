#!/bin/bash

gunicorn dishproject.wsgi:application -b 0.0.0.0:8000 --reload -w 4
