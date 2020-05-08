# Development settings, do not use in production!

from common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nofreeviewnoreview',
        'USER': 'nofreeviewnoreview',
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'DISABLE_SERVER_SIDE_CURSORS': False,
    }
}

ALLOWED_HOSTS = ['nfvnr.dissem.in', 'no-free-view-no-review.org']

ORCID_BASE_DOMAIN = 'orcid.org'

SOCIALACCOUNT_PROVIDERS = \
    {'orcid':
       {
        'BASE_DOMAIN': ORCID_BASE_DOMAIN,
        'MEMBER_API': False
       }
    }

