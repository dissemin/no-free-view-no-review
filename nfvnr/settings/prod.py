from .common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nofreeviewnoreview',
        'USER': 'nofreeviewnoreview',
        'PASSWORD': '',
        'HOST': '',
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

EMAIL_HOST = ''
EMAIL_PORT = 443
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

