from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Barang
from .form import BarangForm


class InvManageView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "inventory/inv_manage.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

class InvAddView(LoginRequiredMixin, CreateView):
    form_class = BarangForm
    template_name = "inventory/inv_add.html"
    def post(self, request, *args, **kwargs):
        username = request.POST['nama']
        password = request.POST['keterangan']
        print(username, password)

class InvDeleteView(LoginRequiredMixin, DeleteView):
    model = Barang
    template_name = "inventory/inv_delete_confirmation.html"
    success_url = reverse_lazy('inventory:manage')

class InvDetailView(LoginRequiredMixin, DetailView):
    model = Barang
    template_name = "inventory/inv_detail.html"
    context_object_name = 'barang'
