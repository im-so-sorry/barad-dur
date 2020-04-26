"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see./
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os
import uuid
from datetime import timedelta
from distutils.util import strtobool

import dj_database_url
from django.utils.translation import ugettext_lazy as _
from kombu import Exchange, Queue

from environs import Env

SERVICE_PREFIX = "ftp-service"

env = Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get("DEBUG", "True"))

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

FILES_DIR = os.path.join(BASE_DIR, "files")

if not os.path.exists(FILES_DIR):
    os.mkdir(FILES_DIR)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["*"])

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "app/templates"),)
# Application definition

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.sitemaps",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Thered part apps
    "rest_framework",
    "django_filters",
    "rest_framework_filters",
    "django_celery_beat",
    # 'debug_toolbar',
    # Apps
    "apps.core",
    "apps.user",
    "apps.project",
    "apps.social",
    "apps.stream",
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "apps.core.middleware.ProcessSocialUserMiddleware",
    "apps.core.middleware.InternalTokenMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {},
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_HOST", "redis://redis:6379/0"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "example",
    },
    "translations_cache": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

print(env("DATABASE_CONNECTION"))
DATABASES = {
    "default": dj_database_url.config(
        default=env(
            "DATABASE_CONNECTION",
            "postgres://postgres:postgres@postgres:5432/postgres",
        ),
        engine="django.db.backends.postgresql_psycopg2",
        conn_max_age=600,
    )
}

# Celery settings

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BEAT_SCHEDULE = {
    "check_new_documents": {
        "project": "apps.project.tasks.new_documents.check_new_documents",
        "schedule": timedelta(minutes=10),
    },
    "check_tasks_statuses": {
        "project": "apps.project.tasks.in_progress_documents.check_tasks_statuses",
        "schedule": timedelta(minutes=10),
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"

# i18
LANGUAGE_CODE = "ru"

USE_I18N = True
LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _("English")),
)

PARLER_LANGUAGES = {1: ({"code": "ru", }, {"code": "en", },)}

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

DATE_FORMAT = "d-m-Y"
USE_L10N = False

ADMIN_ENABLED = os.environ.get("ADMIN_ENABLED", "False") == "True"

SITE_ID = 1

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'apps.core.authentication.XTokenAuthentication',
    # ),
    "DEFAULT_AUTHENTICATION_CLASSES": ("apps.core.authentication.XTokenAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("rest_framework_filters.backends.RestFrameworkFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}
TIME_ZONE = "Europe/Moscow"

FILE_UPLOAD_PERMISSIONS = 0o644

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]

AUTH_USER_MODEL = "user.User"


def show_toolbar(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

UUID_NAMESPACE = uuid.UUID(os.environ.get("UUID_NAMESPACE", "0527cd24-8b69-4c5a-86f8-6842d9388cdf"))

KAFKA_HOSTS = env("KAFKA_HOSTS", "kafka:9092")
KAFKA_GROUP_ID = env("KAFKA_GROUP_ID", "stream_dispatcher")
KAFKA_STREAM_TOPICS = env.list("KAFKA_STREAM_TOPICS", ["vk_stream"])
KAFKA_AUTO_OFFSET_RESET = env("KAFKA_AUTO_OFFSET_RESET", 'earliest')
KAFKA_ENABLE_AUTO_COMMIT = env.bool("KAFKA_ENABLE_AUTO_COMMIT", True)
