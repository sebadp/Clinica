from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER':'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 2021,
    }
}