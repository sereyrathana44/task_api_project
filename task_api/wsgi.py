"""
WSGI config for task_api project.
Gunicorn on the deployment server points at: task_api.wsgi:application
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_api.settings')

application = get_wsgi_application()
