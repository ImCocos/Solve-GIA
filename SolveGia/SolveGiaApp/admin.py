from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from SolveGiaApp.forms import CustomUserCreationForm, CustomUserChangeForm
from SolveGiaApp.models import CustomUser


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username', 'status']
    list_editable = ('status',)


admin.site.register(CustomUser, CustomUserAdmin)
