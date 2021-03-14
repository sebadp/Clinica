from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tpclinica.herokuapp.com']



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db4iqke69dvo79',
        'USER':'gzumsgqkgxctsn',
        'PASSWORD': '8465d9dfeb828c75ea74da533b6bd74f56daf63b909cb508658f9ff087c4ec8d',
        'HOST': 'ec2-52-21-252-142.compute-1.amazonaws.com',
        'PORT': 5432,
    }
}
