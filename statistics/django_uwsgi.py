import os
import sys
from os.path import dirname, abspath

import django
from django.core.handlers.wsgi import WSGIHandler

sys.path.append(dirname(dirname(abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statistics.settings")
django.setup()
application = WSGIHandler()
