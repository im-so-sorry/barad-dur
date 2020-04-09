FROM python:3.7-alpine

WORKDIR /usr/src/app
ENV DATABASE_CONNECTION "sqlite://:memory:"

RUN apk update \
    && apk add ttf-dejavu \
    && apk add openjdk8-jre \
    && apk add libpq postgresql-dev mariadb-connector-c-dev git \
    && apk add build-base openssl-dev libffi-dev unixodbc-dev

ADD . /usr/src/app
RUN pip install -r requirements.txt

RUN python manage.py collectstatic

CMD ["uwsgi", "--socket=0.0.0.0:8000", "--protocol=http", "--lazy", "--module=app.wsgi:application", "--env", "DJANGO_SETTINGS_MODULE=app.settings", "--enable-threads", "--threads=5", "--static-map=/printer/static=/usr/src/app/static"]
