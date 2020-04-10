from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .form import LoginForm
from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect, HttpResponseNotFound

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('inventory:barang_list')

    def form_valid(self, form):
        self.form = form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(self.request, user)
            url_return = reverse_lazy('inventory:barang_list')
        else:
            url_return = reverse_lazy('users:login')
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        auth.logout(request)
        return redirect('/')