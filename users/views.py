from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class LoginView(TemplateView):
    template_name = "users/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.warning(request, 'Username atau Password Salah!')
                return redirect('/')
        else:
            messages.warning(request, 'Username atau Password Kosong!')
            return redirect('/')


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        auth.logout(request)
        return redirect('/')