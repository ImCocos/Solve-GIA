from django.shortcuts import render, get_object_or_404, redirect
import random
from SolveGiaApp.models import *


def index(request):
    return render(request=request, template_name='index.html')


def generate_random_variant(request, category):
    tasks: list[Task] = []
    for type_number in range(1, 26):
        tasks.append(random.choice(list(Task.objects.filter(category=category, type_number=type_number))))

    context = {
        'title': f'Variant of {category}',
        'tasks': tasks,
    }

    return render(request=request, template_name='show-variant.html', context=context)
