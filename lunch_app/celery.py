from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunch_app.settings')

app = Celery('lunch_app')

# Configure logging to a file
#logging.basicConfig(filename='celery.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

