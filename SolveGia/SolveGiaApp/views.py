from django.db import connection, reset_queries
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
import random

from django.urls import reverse_lazy
from django.views.generic import CreateView

from SolveGiaApp.forms import CustomUserCreationForm
from SolveGiaApp.models import *
from django.conf import settings

User = settings.AUTH_USER_MODEL
RUSSIAN_ALPHABET = list('абвгдеёжзийклмнопрстуфхцчшщьыъэюя'.upper())

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
        if cat in [ctg.name for ctg in all_cats]:
            if request.GET.get('SUBMIT') == 'gen':
                return generate_random_variant(request, cat, request.GET.get('difficulty[]'), True)
            elif request.GET.get('SUBMIT') == 'show':
                return redirect('all-variants', cat)
            elif request.GET.get('SUBMIT') == 'const':
                return redirect('constructor', cat)
        if request.GET.get('SUBMIT') == 'show-smns-vars':
            return redirect('show-smns-vars', request.GET.get('pk'))
        elif request.GET.get('SUBMIT') == 'task':
            return redirect('task', request.GET.get('pk'))
        elif request.GET.get('SUBMIT') == 'variant':
            return redirect('variant', request.GET.get('pk'))
    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
    return render(request=request, template_name='index.html', context=context)


"""
Генератор рандомных вариантов и вывод на страницу(сохраняются в качестве строки (12.253.653.167.24.65)
"""


def generate_random_variant(request, category, difficulty: int = None, answers=True):
    check_category(category)
    tasks: list[Task] = []
    ctg: Category = Category.objects.get(name=category)
    if difficulty is not None:
        for type_number in range(1, ctg.max_type_number + 1):
            tasks.append(get_task_closets_to_difficulty(type_number, difficulty))
    else:
        for type_number in range(1, ctg.max_type_number + 1):
            edges = Category.objects.get(name=category).get_edges()[type_number - 1]
            tasks.append(Task.objects.get(pk=random.randint(edges[0], edges[1])))

    str_list_of_pks = '.'.join([str(task.pk) for task in tasks])
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
    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
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

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
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

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
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

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
    return render(request=request, template_name='show-variant.html', context=context)


"""
Функция вывода на страницу всех вариантов(по категории) в виде ссылки на сам вариант
"""


def show_all_variants_of_category(request, category):
    check_category(category)
    ctg = Category.objects.get(name=category)
    variants = Variant.objects.filter(category=ctg, owned_by=False)

    context = {
        'title': f'All variants of {category}',
        'variants': variants,
    }

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
    return render(request=request, template_name='all-variants-of-category.html', context=context)


def check_category(cat):
    if cat not in [ctg.name for ctg in Category.objects.all()]:
        raise Http404


def create_variant(request, category):
    check_category(category)
    ctg = Category.objects.get(name=category)
    edges = ctg.get_edges()

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
                                      owned_by=True)
                new_variant.save()
                add_variant_to_library(request.user, new_variant)

        context = {
            'title': f'Variant constructor for {category}',
            'edges': edges,
            'tasks': tasks,
            'answers': True,
        }

        print(f'Sent queries: {len(connection.queries)}')
        [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
        reset_queries()
        return render(request=request, template_name='show-variant.html', context=context)

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()
    return render(request=request, template_name='create-variant.html', context=context)


def solve_variant(request, pk):
    variant = get_object_or_404(Variant, pk=pk)
    task_pks = variant.get_list_of_tasks_pk()
    user = request.user

    tasks = [Task.objects.get(pk=pk) for pk in task_pks]

    context = {
        'title': f'Variant {variant.pk} of {variant.category.name}',
        'tasks': tasks,
    }

    if request.method == 'GET' and request.GET.get('check') is not None:
        answers = []
        for i in [task.type_number for task in tasks]:
            answers.append(request.GET.get(f'answer{i}'))
        right_answers = [task.answer for task in tasks]

        context['title'] = 'Results'
        context['answers'] = [
            [tasks[i].get_str_type_number(), right_answers[i].replace('<br>', '').replace('<br/>', ''), answers[i],
             valid_answer(answers[i], right_answers[i])] for i in
            range(0, len(right_answers))]

        context['ratio'] = f'{len([ans[3] for ans in context["answers"] if ans[3]])}/{len(right_answers)}'

        if list(user.home_work.all()) is not []:
            if variant.pk in user.home_work.all().values_list('variant_id', flat=True):
                hw: HomeWork = user.home_work.get(variant=variant)
                hw.tries = hw.tries + 1
                right = 0
                for i in context['answers']:
                    if i[3]:
                        right += 1
                hw.result = (right / len(context['answers'])) * 100
                hw.save()

        return render(request, template_name='show-answers.html', context=context)

    print(f'Sent queries: {len(connection.queries)}')
    [print(f'{ind + 1}:{query}\n') for ind, query in enumerate(connection.queries)]
    reset_queries()

    return render(request=request, template_name='solve-variant.html', context=context)


def add_variant_to_library(user: CustomUser, variant):
    user.variants.add(variant)


def show_library(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    library = list(user.variants.all())

    context = {
        'title': f'All variants from {user.username}',
        'variants': [var for var in library],
        'answers': True,
    }

    return render(request, template_name='show-smns-vars.html', context=context)


def rate(mark: int, task: Task, user: User):
    if not user.is_authenticated:
        return False
    if task.voices.filter(pk=user.pk).exists():
        return False
    if mark < 1 or mark > 10:
        return False

    task.voices.add(user)
    task.rating = (task.rating + mark) // 2
    task.save()

    return True


def get_task_closets_to_difficulty(type_number, difficulty):
    tasks_of_type_number_ordered: list[Task] = list(
        Task.objects.filter(type_number=type_number, rating__lte=difficulty).order_by(
            '-rating'))
    max_rating = tasks_of_type_number_ordered[0].rating
    tasks = []
    for task in tasks_of_type_number_ordered:
        if task.rating == max_rating:
            tasks.append(task)
    return random.choice(tasks)


def valid_answer(answer, right_answer):
    answer, right_answer = str(answer), str(right_answer)
    answer, right_answer = answer.lower(), right_answer.lower()

    right_answer = right_answer.replace('<br>', '')
    right_answer = right_answer.replace('<br/>', '')

    if answer == right_answer:
        return True
    else:
        return False


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/reg.html'


def profile(request):
    if not request.user.is_authenticated:
        return Http404
    else:
        user: CustomUser = request.user

    groups = GroupCU.objects.all()

    context = {
        'title': f'{user.username}',
        'user': user,
        'groups': groups,
        'error': '',
        'variants': [hw.variant for hw in user.home_work.all()] if user.home_work is not None else [],
        'russian_alphabet': RUSSIAN_ALPHABET,
        'classes': list(range(1, 12)),
        'cats': list(Category.objects.all().values_list('name', flat=True)),
        'vars_edges':
            (Variant.objects.first().pk, Variant.objects.latest('pk').pk) if Variant.objects.first() is not None else (
                0, 0),
    }

    if user.status >= 2:
        lst = []
        for group in user.groups.all():
            lst.append([group, [get_object_or_404(CustomUser, pk=us_pk) for us_pk in group.get_students_pk()]])
        context['groups_table'] = lst

    if request.method == 'GET':
        if request.GET.get('SUBMIT') == 'set-status':
            status = request.GET.get('status[]')
            if status != '' and status is not None:
                status = int(status)
                if status == 1:
                    user.status = 1
                    user.save()
                elif status == 2 or status == 3:
                    return redirect('confirm', status)
                else:
                    return Http404

            return redirect('profile')

        elif request.GET.get('SUBMIT') == 'create-group' and (user.status == 2 or user.status == 3):
            group_number = request.GET.get('class[]')
            group_let = request.GET.get('letter[]')
            group_cat = request.GET.get('cat[]')

            try:
                group_number = int(group_number)
            except TypeError:
                return Http404

            if group_number not in list(range(1, 12)):
                return Http404

            if group_let not in RUSSIAN_ALPHABET:
                return Http404

            if group_cat not in context['cats']:
                return Http404

            group_name = f'{group_number}-{group_let}-{group_cat}'

            if group_name not in GroupCU.objects.values_list('name', flat=True):
                new_group = GroupCU(name=group_name)
                new_group.save()
                user.groups.add(new_group)
                user.save()
            else:
                context['error'] = 'This name is already taken'

            return redirect('profile')

        elif request.GET.get('SUBMIT') == 'set-hw' and (user.status == 2 or user.status == 3):
            group_pk = int(request.GET.get('set-hw-for-group[]'))
            variant_pk = int(request.GET.get('hw-variant-id'))

            group: GroupCU = GroupCU.objects.get(pk=group_pk)
            variant = get_object_or_404(Variant, pk=variant_pk)

            for member_pk in group.get_students_pk():
                user = CustomUser.objects.get(pk=member_pk)
                new_hw = HomeWork(variant=variant)
                new_hw.save()
                user.home_work.add(new_hw)
                user.save()

            group.group_hws.add(variant)
            group.save()

            return redirect('profile')

        elif request.GET.get('SUBMIT') == 'add-smn' and (user.status >= 2):
            try:
                group_pk = int(request.GET.get('add-smn-to-group[]'))
            except TypeError:
                return Http404

            if group_pk not in list(user.groups.values_list('pk', flat=True)):
                return Http404

            try:
                user_pk = int(request.GET.get('user-pk'))
            except TypeError:
                return Http404

            group = GroupCU.objects.get(pk=group_pk)
            cuser = get_object_or_404(CustomUser, pk=user_pk)

            if cuser.pk not in group.get_students_pk():
                group.students = group.students + f'{cuser.pk}.'
                group.save()
            else:
                context['error'] = 'Student already in group'

            return redirect('profile')
    return render(request, template_name='registration/profile.html', context=context)


def confirm_status(request):
    if not request.user.is_authenticated:
        return Http404

    return render(request, template_name='registration/confirmation.html')


def show_results_of_group(request, group_pk):
    user = request.user
    group: GroupCU = get_object_or_404(GroupCU, pk=group_pk)

    if not user.is_authenticated:
        return Http404

    if not user.status >= 2:
        return Http404
    context = {
        'title': f'Results of group {group.name}',
    }

    homeworks: list[Variant] = list(group.group_hws.all())
    students: list[CustomUser] = [get_object_or_404(CustomUser, pk=user_pk) for user_pk in group.get_students_pk()]
    if len(homeworks) > 0 and len(students) > 0:
        results_table = []
        for hw in homeworks:
            mini_list = [hw, [[student, student.home_work.get(variant=hw)] for student in students]]

            results_table.append(mini_list)

        context['results_table'] = results_table

    return render(request, template_name='show-group-results.html', context=context)
