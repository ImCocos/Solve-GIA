from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('task/<str:category>/<int:id>', show_task),
    path('parse', parse)
]