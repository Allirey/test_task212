from django import forms
from django.contrib.auth.forms import UserCreationForm as CreateForm, UserChangeForm as ChangeForm
from .models import User


class UserCreationForm(CreateForm):
    class Meta(CreateForm):
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'birth_date',

        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'birth_date',
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
