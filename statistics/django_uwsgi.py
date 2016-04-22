import os
import sys

import django
from django.core.handlers.wsgi import WSGIHandler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statistics.settings")
django.setup()
application = WSGIHandler()
