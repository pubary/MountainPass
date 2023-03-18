from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users


class UsersCreationForm(UserCreationForm):
    username = forms.CharField(label='Login')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Users
        fields = ['username',
                  'email',
                  ]


class UsersChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('username', )
