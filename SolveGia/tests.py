import os
import random
import django
import requests
from bs4 import BeautifulSoup
from django.db.models import Max
import sqlite3 as sql

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolveGia.settings')
django.setup()

from SolveGiaApp.models import *

# edges = []
# for i in range(1, 26):
#     tasks = Task.objects.filter(type_number=i)
#     edge = [tasks.first().pk, tasks.latest('pk').pk]
#     edges.append(edge)
#
# print(edges)
#
# string = ''
# for index, edge in enumerate(edges):
#     string += f'{edge[0]}.{edge[1]}+'
#
# print(string)
#
# ctg = Category(name='Informatika', max_type_number=25, edges=string[:-1])
# ctg.save()

# RUSSIAN_ALPHABET = list('абвгдеёжзийклмнопрстуфхцчшщьыъэюя'.upper())
# print(RUSSIAN_ALPHABET)

