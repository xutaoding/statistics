import os

from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statistics.settings")

application = WSGIHandler()
