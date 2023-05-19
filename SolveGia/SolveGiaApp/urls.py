from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('genvar/<str:category>', generate_random_variant, name='genvar'),
    path('task/<int:pk>', show_task, name='task'),
    path('tasks/<str:category>/<int:type_number>', show_all_tasks_of_type, name='show-tasks'),
    path('variant/<int:pk>', show_variant, name='variant'),
    path('variants/<str:category>', show_all_variants_of_category, name='all-variants'),
]
