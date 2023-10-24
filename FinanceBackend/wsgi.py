"""
WSGI config for FinanceBackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

from FinanceBackend.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinanceBackend.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'static'))
