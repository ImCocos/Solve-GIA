import os

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolveGia.settings')
django.setup()

from SolveGiaApp.models import Task

Tasks = Task.objects.all()
for task in Tasks:
    if task.photos != '':
        task.text = task.text.replace('.gif">', '.gif"><br>')
        task.text = task.text.replace('.gif"/>', '.gif"><br>')

    task.save()
    print(task.pk)