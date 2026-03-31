import os
import django
from django.conf import settings

# Configure Django settings before importing test modules
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dividends.settings')
    django.setup()
