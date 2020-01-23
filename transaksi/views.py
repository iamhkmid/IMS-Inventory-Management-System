from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import *
from .form import PeminjamanForm, HabispakaiForm


class TransaksiListView(LoginRequiredMixin, ListView):
    model = Transaksi
    template_name = "transaksi/trans_list.html"
    context_object_name = 'transaksi_list'
    ordering = ['id_transaksi']

class FormPeminjamanView(LoginRequiredMixin, CreateView):
    form_class = PeminjamanForm
    template_name = "transaksi/form_peminjaman.html"

class FormHabispakaiView(LoginRequiredMixin, CreateView):
    form_class = HabispakaiForm
    template_name = "transaksi/form_habispakai.html"

class TransDetail(LoginRequiredMixin, DetailView):
    model = Transaksi
    template_name = "transaksi/Trans_detail.html"
    context_object_name = 'transaksi'