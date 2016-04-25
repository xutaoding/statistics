import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/root/.pyenv/versions/anaconda-2.3.0/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statistics.settings")

import django
from django.core.handlers.wsgi import WSGIHandler

django.setup()
application = WSGIHandler()
