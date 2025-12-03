# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CouchCraft_AI.settings')

app = Celery('CouchCraft_AI')

# Carica configurazione da settings.py con prefisso CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Scopre automaticamente tasks.py nelle app
app.autodiscover_tasks()

