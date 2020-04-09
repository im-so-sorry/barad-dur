from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from app import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("ftp_client")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(settings.INSTALLED_APPS)
