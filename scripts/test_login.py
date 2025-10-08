import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django

django.setup()
from django.test import Client

c = Client()
resp = c.post('/api/root/login/', {'username':'suzan','password':'20311678'}, content_type='application/json')
print('status', resp.status_code)
print(resp.content)
