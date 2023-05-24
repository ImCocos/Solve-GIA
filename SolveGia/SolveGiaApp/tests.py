import os

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolveGia.settings')
django.setup()

from SolveGiaApp.models import *


# def set_tasks_edges(category_name):
#     tasks_edges: list[[int, int]] = []
#     last_number = Task.objects.filter(category=category_name).latest('type_number').type_number
#     for tn in range(1, last_number + 1):
#         tpt = Task.objects.filter(category=category_name, type_number=tn)
#         edges = [int(tpt.first().pk), int(tpt.latest('pk').pk)]
#         tasks_edges.append(edges)
#     string = ''
#     for task_edges in tasks_edges:
#         string += str(task_edges[0]) + '.' + str(task_edges[1]) + '+'
#
#     string = string[:-1]
#
#     return string
#
#
# new_cat_edges = set_tasks_edges('Informatika')
#
# new_cat = Category(name='Informatika', edges=new_cat_edges)
# new_cat.save()
# print(new_cat.name, new_cat.edges, new_cat.get_edges())

# cat = Category.objects.get(pk=1)
# print(cat, cat.get_edges())
#
# for task in list(Task.objects.all()):
#     task.category = cat
#     task.save()
# for var in list(Variant.objects.all()):
#     var.category = cat
#     var.save()

# task = KindaTask.objects.get(pk=1)
#
# cuser = KindaUser.objects.get(pk=499)
# import time
# print(f'START TIME SET')
# start = time.time()
# print(cuser in task.voices.all(), time.time()-start)
