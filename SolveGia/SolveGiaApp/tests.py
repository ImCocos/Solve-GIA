import os

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolveGia.settings')
django.setup()

from SolveGiaApp.models import Task
