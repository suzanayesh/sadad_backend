import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django

django.setup()
from apps.admin_users.models import RootUserToken

for key, root_id in RootUserToken.objects.values_list('key','root_user__id'):
    print(f"{key} (root_id={root_id})")
