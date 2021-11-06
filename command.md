# 一些指令

## Python
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`

## Django
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## Vue
- `npm i`
- `npm run serve`
- `npm run build`

## Nginx
- Linux
    - `service nginx start`
    - `service nginx stop`
    - `service nginx restart`
    - `service nginx status`
    - `nginx -s reload`
- Windows
    - `taskkill /f /im nginx.exe`
    
## Web
- `daphne project.asgi:application -b 0.0.0.0 -p 8081`
- `uwsgi --ini uwsgi.ini`

## Docker
- `docker build -t test .`
- `docker run -p 48763:48763 test`