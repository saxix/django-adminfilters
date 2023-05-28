import os
import sys
from pathlib import Path
from uuid import uuid4

from environ import environ

here = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(here, "..", "..")))

BASE_DIR = Path(__file__).resolve(strict=True).parents[3]

env = environ.Env(
    DEBUG=(bool, False),
    STATIC_ROOT=(str, str(BASE_DIR / "~build" / "staticfiles")),
    DATABASE_URL=(str, ""),
    ROOT_TOKEN=(str, uuid4().hex),
)

DEBUG = env("DEBUG")
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ["*"]

TIME_ZONE = "Asia/Bangkok"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(here, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = env("STATIC_ROOT")
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATICFILES_DIRS = ()

SECRET_KEY = "c73*n!y=)tziu^2)y*@5i2^)$8z$tx#b9*_r3i6o1ohxo%*2^a"
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

DATABASES = {"default": env.db()}
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

ROOT_URLCONF = "demo.urls"
WSGI_APPLICATION = "demo.wsgi.application"

AUTHENTICATION_BACKENDS = ("demo.backends.AnonymousAccessUserBackend",)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "adminfilters",
    "adminfilters.depot",
    "demo",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
    "pytest_selenium": {
        "handlers": ["console"],
        "level": "ERROR",
    },
}
