from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
import random
from SolveGiaApp.models import *

"""
Очевидно простая функция вывода индекс страницы, request обязательно принимать в каждой функции
"""


def index(request):
    all_cats = list(Category.objects.all())
    context = {
        'title': 'Main page',
        'cats': all_cats,
    }
    if request.method == 'GET' and request.GET.get('SUBMIT') is not None:
        cat = request.GET.get('subject[]')
        if cat in [ctg.name for ctg in Category.objects.all()]:
            if request.GET.get('SUBMIT') == 'gen':
                return redirect('genvar', cat)
            elif request.GET.get('SUBMIT') == 'show':
                return redirect('all-variants', cat)
            elif request.GET.get('SUBMIT') == 'const':
                return redirect('constructor', cat)
        if request.GET.get('SUBMIT') == 'show-smns-vars':
            return redirect('show-smns-vars', request.GET.get('pk'))
    return render(request=request, template_name='index.html', context=context)


"""
Генератор рандомных вариантов и вывод на страницу(сохраняются в качестве строки (12.253.653.167.24.65)
"""


def generate_random_variant(request, category, answers=True):
    check_category(category)
    tasks: list[Task] = []
    for type_number in range(1, 26):
        edges = Category.objects.get(name=category).get_edges()[type_number - 1]
        tasks.append(
            Task.objects.get(type_number=type_number,
                             pk=random.randint(edges[0], edges[1])))

    str_list_of_pks = '.'.join([str(task.pk) for task in tasks])
    ctg = Category.objects.get(name=category)
    var = Variant(variant=str_list_of_pks, category=ctg)
    var.save()

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
    error = ''
    if request.method == 'GET' and request.GET.get('RATE') is not None:
        mark = int(request.GET.get('mark'))
        error = '' if rate(mark, task, request.user) else 'You can\'t rate twice or you aren\'t authorized'

    context = {
        'title': f'Task {task.get_str_type_number()}.{task.pk}({task.rating}) of {task.category.name}',
        'task': task,
        'error': error,
    }

    return render(request=request, template_name='show-task.html', context=context)


"""
Функция вывода всех заданий конкретного типа и конкретной категории, очевидно по типу и категории
"""


def show_all_tasks_of_type(request, category, type_number):
    check_category(category)
    ctg = Category.objects.get(name=category)
    latest_tn = Task.objects.filter(category=ctg).latest('type_number').type_number
    if type_number < 1 or type_number > latest_tn:
        raise Http404

    """
    Из-за того что Поляков соединил 3 задания в одно, приходится писать такие костыли
    """

    tasks = Task.objects.filter(category=ctg, type_number=type_number)

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
        'title': f'Variant {variant.pk} of {variant.category.name}',
        'tasks': tasks,
        'answers': True,
    }

    return render(request=request, template_name='show-variant.html', context=context)


"""
Функция вывода на страницу всех вариантов(по категории) в виде ссылки на сам вариант
"""


def show_all_variants_of_category(request, category):
    check_category(category)
    ctg = Category.objects.get(name=category)
    variants = Variant.objects.filter(category=ctg, owned=False)

    context = {
        'title': f'All variants of {category}',
        'variants': variants,
    }

    return render(request=request, template_name='all-variants-of-category.html', context=context)


def check_category(cat):
    if cat not in [ctg.name for ctg in Category.objects.all()]:
        raise Http404


def create_variant(request, category):
    check_category(category)
    edges = Category.objects.get(name=category).get_edges()
    ctg = Category.objects.get(name=category)

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
                tasks.append(Task.objects.get(category=ctg, pk=int(request.GET.get(name))))
        add_to_lib = request.GET.get('add-to-lib')
        if add_to_lib == 'add':
            if request.user.is_authenticated and len(tasks) != 0:
                new_variant = Variant(category=ctg, variant='.'.join([str(task.pk) for task in tasks]),
                                      owned=True)
                new_variant.save()
                add_variant_to_library(request.user, new_variant)

        context = {
            'title': f'Variant constructor for {category}',
            'edges': edges,
            'tasks': tasks,
            'answers': True,
        }
        return render(request=request, template_name='show-variant.html', context=context)

    return render(request=request, template_name='create-variant.html', context=context)


def add_variant_to_library(user: User, variant):
    if user not in list([library.owner for library in Library.objects.all()]):
        owner = Library(owner=user)
        owner.save()
    else:
        owner = Library.objects.get(owner=user)

    owner.variants.add(variant)
    owner.save()


def show_library(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    library = Library.objects.get(owner=user)

    context = {
        'title': f'All variants from {user.username}',
        'variants': [var for var in library.variants.all()],
        'answers': True,
    }

    return render(request, template_name='show-smns-vars.html', context=context)


def rate(mark: int, task: Task, user: User):
    if not user.is_authenticated:
        return False
    if user in task.voices.all():
        return False
    if mark < 1 or mark > 10:
        return False

    task.voices.add(user)
    task.rating = (task.rating + mark) // 2
    task.save()

    return True
