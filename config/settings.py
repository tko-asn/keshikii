from pathlib import Path
import os
from .base_settings import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ['*']


try:
    from .local_settings import *
except ImportError:
    pass


if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY']

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

    AWS_CLOUDFRONT_DOMAIN = os.environ['AWS_CLOUDFRONT_DOMAIN']

    # AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400', 
    }
    AWS_LOCATION = 'media'

    MEDIA_URL = "https://{}/{}/".format(AWS_CLOUDFRONT_DOMAIN, AWS_LOCATION)
    # MEDIA_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    import django_heroku
    django_heroku.settings(locals())
