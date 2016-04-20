from django.test import TestCase
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import QueryDict


import requests

# Create your tests here.
print requests.post('http://127.0.0.1:7900/news/api/data.json', data={'dd': 100, 'csrftoken': 'abc'})