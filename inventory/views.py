from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Barang
from .form import BarangForm


class InventoryList(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "inventory/inventory_list.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

class TambahBarang(LoginRequiredMixin, CreateView):
    form_class = BarangForm
    template_name = "inventory/tambah_barang.html"
