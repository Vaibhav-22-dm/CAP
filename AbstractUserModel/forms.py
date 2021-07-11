from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'middle_name', 'last_name', 'phone', 'city', 'college', 'facebook', 'linkedin', 'image')
