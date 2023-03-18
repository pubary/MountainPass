from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsersCreationForm, UsersChangeForm
from .models import Users


class UsersAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = Users
    list_display = ['email', 'username',]


admin.site.register(Users, UsersAdmin)
