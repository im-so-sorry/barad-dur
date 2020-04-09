#!/usr/bin/env bash

FUNCTION=
if [ ! -z $1 ]; then
  FUNCTION="$1"
fi

show-help() {
  echo 'Celery functions:'
  echo './run_celery.sh [worker] [beat] [flower]'
}

worker() {
  celery -A apps.core worker -l info
}

beat() {
  celery -A apps.core beat -l info
}
flower() {
  celery -A apps.core flower -l info
}

case "$1" in
-h | --help)
  show-help
  ;;
*)
  if [ ! -z $(type -t $FUNCTION | grep function) ]; then
    $1
  else
    show-help
  fi
  ;;
esac
