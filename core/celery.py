"""Celery configuration."""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kathmandu')

app.autodiscover_tasks()
