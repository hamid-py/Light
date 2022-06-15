import os
from celery import Celery
from django.shortcuts import redirect, render


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticker.settings')
app = Celery("sticker", broker="amqp://localhost")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

