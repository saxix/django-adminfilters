# Django settings for demoproject project.
import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(here, '..', '..')))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'DEMODB.sqlite',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Asia/Bangkok'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(here, 'media')
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
SECRET_KEY = 'c73*n!y=)tziu^2)y*@5i2^)$8z$tx#b9*_r3i6o1ohxo%*2^a'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',)

ROOT_URLCONF = 'demoproject.urls'
WSGI_APPLICATION = 'demoproject.wsgi.application'

AUTHENTICATION_BACKENDS = ('demoproject.backends.AnyUserBackend',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'adminfilters',
    'demoproject.demoapp')

# Django 1.9

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates',
     'DIRS': [],
     'APP_DIRS': True,
     'OPTIONS': {
         'debug': DEBUG,
         'context_processors': [
             'django.contrib.auth.context_processors.auth',
             'django.template.context_processors.debug',
             'django.template.context_processors.i18n',
             'django.template.context_processors.media',
             'django.template.context_processors.static',
             'django.template.context_processors.tz',
             'django.contrib.messages.context_processors.messages',
         ],
     },
     }
]
