import os

from .base import *  # noqa: F403

# Fixo: DEBUG nunca deve depender de variável de ambiente esquecida em produção
# (esse foi um problema real identificado no projeto anterior — ver checklist de segurança)
DEBUG = False

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(
    ",")  # falha alto se não configurado

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
