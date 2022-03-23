"""
WSGI config for django_k8s_sample project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import pathlib
import dotenv


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_k8s_sample.settings')

CURRENT_DIR= pathlib.Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
ENV_FILE_PATH = BASE_DIR / ".venv"

dotenv.read_dotenv(str(ENV_FILE_PATH))

application = get_wsgi_application()
