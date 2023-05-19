from django.http import Http404
from django.shortcuts import render, get_object_or_404
import random
from SolveGiaApp.models import *


"""
Массив с категориями заданий, который потом надо будет заменить на отдельную таблицу в БД
"""


LIST_OF_CATEGORIES = ['Informatika']


"""
Границы заданий по pk(на каждое задание по две границы(верхняя и нижняя))
В будущем заменить на отдельную таблицу в бд
"""


TASKS_EDGES: list[tuple[int, int]] = []
for tn in range(1, 26):
    tpt = Task.objects.filter(type_number=tn)
    edges = int(tpt.first().pk), int(tpt.latest('pk').pk)
    TASKS_EDGES.append(edges)


"""
Очевидно простая функция вывода индекс страницы, request обязательно принимать в каждой функции
"""


def index(request):
    return render(request=request, template_name='index.html')


"""
Генератор рандомных вариантов и вывод на страницу(сохраняются в качестве строки (12.253.653.167.24.65)
"""


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


    """
    Контекст очень полезная вещь, передаёт в html файл данные через переменные    
    """


    context = {
        'title': f'Variant of {category}',
        'tasks': tasks,
        'answers': answers,
    }

    return render(request=request, template_name='show-variant.html', context=context)


"""
Функция вывода конкретного задания на страницу через его pk
"""


def show_task(request, pk):
    task = get_object_or_404(Task, pk=pk)


    """
    При неверном pk функция get_object_or_404 вместо ошибки вернет страницу 404 
    """


    context = {
        'title': f'Task {task.get_str_type_number()}.{task.pk} of {task.category}',
        'task': task,
    }

    return render(request=request, template_name='show-task.html', context=context)


"""
Функция вывода всех заданий конкретного типа и конкретной категории, очевидно по типу и категории
"""


def show_all_tasks_of_type(request, category, type_number):
    latest_tn = Task.objects.filter(category=category).latest('type_number').type_number
    latest_tn += 2 if category == 'Informatika' else 0
    if type_number < 1 or type_number > latest_tn:
        raise Http404


    """
    Из-за того что Поляков соединил 3 задания в одно, приходится писать такие костыли
    """


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


"""
Вывод СУЩЕСТВУЮЩЕГО варианта через его pk
"""


def show_variant(request, pk):
    variant = get_object_or_404(Variant, pk=pk)


    """
    Функция get_list_of_tasks_pk вернет массив состоящий из pk который создаётся из строки
    (см. пример над функцией generate_random_variant)
    """


    task_pks = variant.get_list_of_tasks_pk()

    tasks = [Task.objects.get(pk=pk) for pk in task_pks]

    context = {
        'title': f'Variant of {variant.category}({variant.pk})',
        'tasks': tasks,
        'answers': True,
    }

    return render(request=request, template_name='show-variant.html', context=context)


"""
Функция вывода на страницу всех вариантов(по категории) в виде ссылки на сам вариант
"""


def show_all_variants_of_category(request, category):
    variants = Variant.objects.filter(category=category)

    context = {
        'title': f'All variants of {category}',
        'variants': variants,
    }

    return render(request=request, template_name='all-variants-of-category.html', context=context)
