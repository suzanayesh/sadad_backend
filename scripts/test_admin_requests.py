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
    # get legacy token
    resp = client.post('/api/root/login/', data='{"username":"suzan","password":"20311678"}', content_type='application/json')
    print('/api/root/login/ ->', resp.status_code, resp.content)
    if resp.status_code == 200:
        token = resp.json().get('token')
        # call protected endpoint using Authorization header
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        resp2 = client.get('/api/root/1/admin-requests/', **headers)
        print('/api/root/1/admin-requests/ ->', resp2.status_code)
        print(resp2.content)
    else:
        print('Could not obtain token')
