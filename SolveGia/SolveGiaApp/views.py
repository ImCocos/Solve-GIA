from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
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


def get_tasks_edges(category):
    tasks_edges: list[tuple[int, int]] = []
    last_number = Task.objects.filter(category=category).latest('type_number').type_number
    for tn in range(1, last_number + 1):
        tpt = Task.objects.filter(category=category, type_number=tn)
        edges = int(tpt.first().pk), int(tpt.latest('pk').pk)
        tasks_edges.append(edges)
    return tasks_edges


DIR_OF_EDGES = {}


def create_edges():
    for category in LIST_OF_CATEGORIES:
        DIR_OF_EDGES[category] = get_tasks_edges(category)


create_edges()

"""
Очевидно простая функция вывода индекс страницы, request обязательно принимать в каждой функции
"""


def index(request):
    if request.method == 'GET' and request.GET.get('SUBMIT') is not None:
        cat = request.GET.get('cat')
        if cat in LIST_OF_CATEGORIES:
            if request.GET.get('SUBMIT') == 'gen':
                return redirect('genvar', cat)
            elif request.GET.get('SUBMIT') == 'show':
                return redirect('all-variants', cat)
            elif request.GET.get('SUBMIT') == 'const':
                return redirect('constructor', cat)
    return render(request=request, template_name='index.html')


"""
Генератор рандомных вариантов и вывод на страницу(сохраняются в качестве строки (12.253.653.167.24.65)
"""


def generate_random_variant(request, category, answers=True):
    check_category(category)
    tasks: list[Task] = []
    for type_number in range(1, 26):
        tasks.append(
            Task.objects.get(type_number=type_number, pk=random.randint(*DIR_OF_EDGES[category][type_number - 1])))

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
    check_category(category)
    latest_tn = Task.objects.filter(category=category).latest('type_number').type_number
    if type_number < 1 or type_number > latest_tn:
        raise Http404

    """
    Из-за того что Поляков соединил 3 задания в одно, приходится писать такие костыли
    """

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
    check_category(category)
    variants = Variant.objects.filter(category=category)

    context = {
        'title': f'All variants of {category}',
        'variants': variants,
    }

    return render(request=request, template_name='all-variants-of-category.html', context=context)


def check_category(cat):
    if cat not in LIST_OF_CATEGORIES:
        raise Http404


def create_variant(request, category):
    check_category(category)
    edges = DIR_OF_EDGES[category]

    tasks: list[Task] = []
    for type_number in range(1, 26):
        tasks.append(
            Task.objects.get(type_number=type_number, pk=random.randint(*edges[type_number - 1])))

    context = {
        'title': f'Variant constructor for {category}',
        'edges': edges,
    }

    if request.method == 'GET' and request.GET.get('SUBMIT') is not None:
        tasks: list[Task] = []
        for edge in enumerate(edges):
            name = 'choice_' + str(edge[1][0])
            if str(request.GET.get(name)) != '':
                tasks.append(Task.objects.get(category=category, pk=int(request.GET.get(name))))
        context = {
            'title': f'Variant constructor for {category}',
            'edges': edges,
            'tasks': tasks,
            'answers': True,
        }
        return render(request=request, template_name='show-variant.html', context=context)

    return render(request=request, template_name='create-variant.html', context=context)
