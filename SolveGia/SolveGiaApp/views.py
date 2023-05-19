from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
import random

from django.views.defaults import page_not_found

from SolveGiaApp.models import *

LIST_OF_CATEGORIES = ['Informatika']

TASKS_EDGES: list[tuple[int, int]] = []
for tn in range(1, 26):
    tpt = Task.objects.filter(type_number=tn)
    edges = int(tpt.first().pk), int(tpt.latest('pk').pk)
    TASKS_EDGES.append(edges)


def index(request):
    return render(request=request, template_name='index.html')


def generate_random_variant(request, category, answers=True):
    tasks: list[Task] = []
    if category not in LIST_OF_CATEGORIES:
        raise Http404
    for type_number in range(1, 26):
        tasks.append(Task.objects.get(type_number=type_number, pk=random.randint(*TASKS_EDGES[type_number - 1])))

    str_list_of_pks = '.'.join([str(task.pk) for task in tasks])
    var = Variant(variant=str_list_of_pks, category=category)
    var.save()
    print(str_list_of_pks)

    context = {
        'title': f'Variant of {category}',
        'tasks': tasks,
        'answers': answers,
    }

    return render(request=request, template_name='show-variant.html', context=context)


def show_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    context = {
        'title': f'Task {task.get_str_type_number()}.{task.pk} of {task.category}',
        'task': task,
    }

    return render(request=request, template_name='show-task.html', context=context)


def show_all_tasks_of_type(request, category, type_number):
    latest_tn = Task.objects.filter(category=category).latest('type_number').type_number
    latest_tn += 2 if category == 'Informatika' else 0
    if type_number < 1 or type_number > latest_tn:
        raise Http404
    if category == 'Informatika':
        if 19 <= type_number <= 21:
            type_number = 19
        elif type_number > 21:
            type_number -= 2

    tasks = Task.objects.filter(category=category, type_number=type_number)

    context = {
        'title': f'Tasks of {category}',
        'tasks': tasks,
    }

    return render(request=request, template_name='show-tasks.html', context=context)


def show_variant(request, pk):
    variant = get_object_or_404(Variant, pk=pk)
    task_pks = variant.get_list_of_tasks_pk()

    tasks = [Task.objects.get(pk=pk) for pk in task_pks]

    context = {
        'title': f'Variant of {variant.category}({variant.pk})',
        'tasks': tasks,
        'answers': True,
    }

    return render(request=request, template_name='show-variant.html', context=context)


def show_all_variants_of_category(request, category):
    variants = Variant.objects.filter(category=category)

    context = {
        'title': f'All variants of {category}',
        'variants': variants,
    }

    return render(request=request, template_name='all-variants-of-category.html', context=context)

