#!/bin/sh
source venv/bin/activate
exec gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - src:application