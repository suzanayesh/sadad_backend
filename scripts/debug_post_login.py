import os
import sys

# Ensure cwd (project root) is on sys.path so 'config' module is importable
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.conf import settings
from django.test import Client
from django.test.utils import override_settings

print('Using settings:', os.environ.get('DJANGO_SETTINGS_MODULE'))
print('INSTALLED_APPS contains:', settings.INSTALLED_APPS[:5])

# The test client uses the host 'testserver' which is not in ALLOWED_HOSTS
# in our config; override it for this debug run to avoid DisallowedHost.
with override_settings(ALLOWED_HOSTS=['testserver']):
	client = Client()
	resp = client.post('/api/root/login/', data='{"username":"suzan","password":"20311678"}', content_type='application/json')
	print('status', resp.status_code)
	print('content:', resp.content)
