from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_LOCAL_NAME'),
        'USER': env.str('DB_LOCAL_USERNAME'),
        'PASSWORD': env.str('DB_LOCAL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 2021,
    }
}