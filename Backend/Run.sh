#! /bin/bash

nohup daphne -b 0.0.0.0 -p 8081 project.asgi:application > daphne_log.txt 2>&1 &

nohup uwsgi --ini uwsgi.ini > uwsgi_log.txt 2>&1 &