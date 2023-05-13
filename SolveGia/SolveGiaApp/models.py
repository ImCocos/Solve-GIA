from django.db import models
from django.urls import reverse
EMPTY_STRING = ''

class Task(models.Model):
    type_number = models.IntegerField(blank=False)
    text = models.TextField(blank=False)
    answer = models.TextField(blank=False)
    photos = models.TextField(blank=True)
    files = models.TextField(blank=True)
    time_median = models.FloatField(blank=True, default=0)
    category = models.TextField(blank=False)

    def get_absolute_url(self):
        return reverse('task', kwargs={'category': self.category.name, 'id': self.__pk})

    def __str__(self):
        return f'<Object[task]:{self.type_number}.{self.pk}>'

    def get_photo_url(self):
        return f'SolveGiaApp/media/tasks/images/{self.photos}'

    def get_file_url(self):
        return [f'SolveGiaApp/media/tasks/files/{file_name}' for file_name in list(str(self.files).split('+'))]
