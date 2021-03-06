FROM python:3.7-alpine

WORKDIR /usr/src/app
ENV DATABASE_CONNECTION "sqlite://:memory:"

RUN apk add --no-cache --virtual .deps gcc musl-dev

RUN apk update \
    && apk add ttf-dejavu \
    && apk add openjdk8-jre \
    && apk add libpq postgresql-dev mariadb-connector-c-dev git \
    && apk add build-base openssl-dev libffi-dev unixodbc-dev

ADD . /usr/src/app
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD ["uwsgi", "uwsgi.ini"]
