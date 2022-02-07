import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(here, '..', '..')))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

db = os.environ.get('DBENGINE', 'pg')
if db == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'adminfilters',
            'HOST': os.environ.get('PG_HOST', '127.0.0.1'),
            'PORT': os.environ.get('PG_PORT', '5432'),
            'USER': os.environ.get('PG_USER', 'postgres'),
            'PASSWORD': os.environ.get('PG_PASSWORD', ''),
        }}
elif db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'adminfilters',
            'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
            'PORT': os.environ.get('MYSQL_PORT', ''),
            'USER': os.environ.get('MYSQL_USER', 'root'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),

            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
            'TEST': {
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            },
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci'}}
elif db == 'myisam':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'adminfilters',
            'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
            'PORT': os.environ.get('MYSQL_PORT', ''),
            'USER': os.environ.get('MYSQL_USER', 'root'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),

            'CHARSET': 'utf8',
            'OPTIONS': {'init_command': 'SET storage_engine=MyISAM'},
            'COLLATION': 'utf8_general_ci',
            'TEST': {
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            },
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci'}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '~adminfilters.sqlite',
            'TEST': {
                'NAME': ':memory:',
            },
            'TEST_NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'ATOMIC_REQUESTS': True}}

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
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',)

ROOT_URLCONF = 'demo.urls'
WSGI_APPLICATION = 'demo.wsgi.application'

AUTHENTICATION_BACKENDS = ('demo.backends.AnonymousAccessUserBackend',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'adminfilters',
    'adminfilters.depot',
    'demo')

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
    'pytest_selenium': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}
