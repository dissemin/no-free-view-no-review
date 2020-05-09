# Development settings, do not use in production!

from .common import *

DEBUG = True

# Disables captchas
CAPTCHA_TEST_MODE = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!m()1-n8ta#+i+1g+4!5n97#-6un_@^+ae(4e1ocy+x_)bl*y8'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ORCID_BASE_DOMAIN = 'sandbox.orcid.org'

SOCIALACCOUNT_PROVIDERS = \
    {'orcid':
       {
        'BASE_DOMAIN': ORCID_BASE_DOMAIN,
        'MEMBER_API': False
       }
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CONFIRMATION_SENDING_EMAIL = 'noreply@dissem.in'
