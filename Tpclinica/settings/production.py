from .base import *


DEBUG = env.bool('DEBUG_PRODUCTION', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_PROD_NAME'),
        'USER': env.str('DB_PROD_USER'),
        'PASSWORD': env.str('DB_PROD_PASSWORD'),
        'HOST': env.str('DB_PROD_HOST'),
        'PORT': 5432,
    }
}
