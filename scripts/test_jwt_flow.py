import os
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.test import Client
from django.test.utils import override_settings

with override_settings(ALLOWED_HOSTS=['testserver']):
    client = Client()
    data = {'username': 'suzan', 'password': '20311678'}
    resp = client.post('/api/token/', data=data, content_type='application/json')
    print('/api/token/ ->', resp.status_code, resp.content)
    if resp.status_code == 200:
        j = resp.json()
        access = j.get('access')
        refresh = j.get('refresh')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access}'}
        resp2 = client.get('/api/root/1/admin-requests/', **headers)
        print('/api/root/1/admin-requests/ ->', resp2.status_code)
        print(resp2.content)
    else:
        print('Could not obtain JWT')
