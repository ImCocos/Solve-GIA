from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('genvar/<str:category>/', generate_random_variant, name='genvar'),
    path('task/<int:pk>/', show_task, name='task'),
    path('tasks/<str:category>/<int:type_number>/', show_all_tasks_of_type, name='show-tasks'),
    path('variant/<int:pk>/', show_variant, name='variant'),
    path('variants/<str:category>/', show_all_variants_of_category, name='all-variants'),
    path('variant-constructor/<str:category>/', create_variant, name='constructor'),
    path('library/<int:user_pk>/', show_library, name='show-smns-vars'),
    path('solve-variant/<int:pk>/', solve_variant, name='solve-variant'),
    path('reg/', SignUpView.as_view(), name='reg'),
    path('login/', LoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('confirm-status/<int:status>/', confirm_status, name='confirm'),
    path('show-results/<int:group_pk>', show_results_of_group, name='results')
]
