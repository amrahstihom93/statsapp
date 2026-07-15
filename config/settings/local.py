"""
Local development settings.
Overrides base settings for local Mac development.
"""
from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ['*']

# Email: print to terminal instead of actually sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
