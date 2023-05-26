from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

EMPTY_STRING = ''


class Category(models.Model):
    name = models.TextField()
    edges = models.TextField()  # example: 12.34+7675.78+823283.23
    max_type_number = models.IntegerField()  # example 26

    def get_edges(self):
        string = self.edges.split('+')
        string = string
        for index, edges in enumerate(string):
            string[index] = edges.split('.')
            for i, edge in enumerate(string[index]):
                string[index][i] = int(edge)

        return string

    def __str__(self):
        return f'<Category-{self.name}>'

    def get_absolute_url(self):
        return reverse('all-variants', kwargs={'category': self.name})


class Task(models.Model):
    type_number = models.IntegerField(blank=False)
    text = models.TextField(blank=False)
    answer = models.TextField(blank=False)
    photos = models.TextField(blank=True)
    files = models.TextField(blank=True)
    rating = models.IntegerField(blank=True, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    voices = models.ManyToManyField(User, blank=True)

    def get_absolute_url(self):
        return reverse('task', kwargs={'id': self.__pk})

    def __str__(self):
        return f'<Object[task]:{self.type_number}.{self.pk}>'

    def get_photo_url(self):
        return str(self.photos).replace('static/', '/static/')

    def get_first_file_url(self):
        return [f'/static/tasks/files/{file_name}' for file_name in list(str(self.files).split('+'))][0]

    def get_second_file_url(self):
        if len([f'/static/tasks/files/{file_name}' for file_name in list(str(self.files).split('+'))]) == 2:
            return [f'/static/tasks/files/{file_name}' for file_name in list(str(self.files).split('+'))][1]
        else:
            return ''

    def append_two(self):
        return int(self.type_number) + 2

    def get_str_type_number(self):
        if self.category.name == 'Informatika':
            if self.type_number < 19:
                return str(self.type_number)
            elif self.type_number > 19:
                return str(self.type_number + 2)
            else:
                return '19-21'

    def get_int_type_number(self):
        if self.category.name == 'Informatika':
            if self.type_number < 19:
                return self.type_number
            elif 19 <= self.type_number <= 21:
                return 19
            elif self.type_number > 21:
                return self.type_number


class Variant(models.Model):
    variant = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    owned = models.BooleanField(default=False)

    def __str__(self):
        return self.variant

    def get_absolute_url(self):
        return reverse('variant', kwargs={'pk': self.pk})

    def get_list_of_tasks_pk(self):
        return list(str(self.variant).split('.'))


class Library(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    variants = models.ManyToManyField(Variant, blank=True)

    def get_absolute_url(self):
        return reverse('show-smns-vars', kwargs={'user_pk': self.pk})

    def __str__(self):
        return f'<Library-of-{self.owner.username}>'
