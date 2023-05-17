from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('genvar/<str:category>', generate_random_variant, name='genvar'),
]