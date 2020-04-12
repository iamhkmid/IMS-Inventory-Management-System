from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .models import *
from datetime import datetime
from django.conf import settings
import pytz

class LoginForm(Form):
    username = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        username_list = User.objects.values_list('username', flat=True)
        if username in username_list:
            check_user = authenticate(username=username, password=password)
            if check_user is None:
                self.add_error('password', "Password salah.")
        else:
            self.add_error('username', "Username tidak ditemukan.")
            self.add_error('password', "")
                