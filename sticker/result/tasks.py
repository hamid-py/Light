import os
from celery import Celery, shared_task
from django.shortcuts import redirect, render

from .models import Group, StartRest

# Load task modules from all registered Django apps.
from .views import IN_rest_list, OUT_rest_list, CRM_rest_list



@shared_task
def rest_start(a, b):
    print(a + b)
    return a + b

