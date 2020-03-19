from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView, RedirectView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .form import *
from datetime import datetime
from reports.models import Mutasi
from django.utils.dateparse import parse_datetime
from django.conf import settings
import pytz
import barcode
from barcode.writer import ImageWriter
from barcode import generate
import os

def user_updated(self):
    if self.request.user.get_full_name() == "":
        nama = self.request.user.username
    else:
        nama = self.request.user.get_full_name()
    return nama

# Create your views here.
class TempatListView(LoginRequiredMixin, ListView):
    model = Tempat
    template_name = "satker/tempat_list.html"
    context_object_name = 'tempat_list'
    ordering = ['id_tempat']


class TempatAddView(LoginRequiredMixin, CreateView):
    form_class = TempatForm
    template_name = "satker/tempat_add.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:tempat_detail', kwargs={'pk': self.object.id_tempat})
        return success_url


class TempatDetailView(LoginRequiredMixin, DetailView):
    model = Tempat
    template_name = "satker/tempat_detail.html"
    context_object_name = 'tempat'


class TempatUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TempatForm
    model = Tempat
    template_name = "satker/tempat_update.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:tempat_detail', kwargs={'pk': self.object.id_tempat})
        return success_url


class TempatDeleteView(LoginRequiredMixin, DeleteView):
    model = Tempat
    template_name = "satker/tempat_del_conf.html"
    success_url = reverse_lazy('satker:tempat_list')

    def dispatch(self, request, *args, **kwargs):
        tempat_obj = Tempat.objects.get(id_tempat=self.kwargs['pk'])
        if tempat_obj.is_used:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>(' + tempat_obj.nama +') Tidak dapat dihapus karena sudah digunakan.</h4>')
        return super().dispatch(request, *args, **kwargs)


class RuangListView(LoginRequiredMixin, ListView):
    model = Ruang
    template_name = "satker/ruang_list.html"
    context_object_name = 'ruang_list'
    ordering = ['id_ruang']


class RuangAddView(LoginRequiredMixin, CreateView):
    form_class = RuangForm
    template_name = "satker/ruang_add.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:ruang_detail', kwargs={'pk': self.object.id_ruang})
        return success_url


class RuangDetailView(LoginRequiredMixin, DetailView):
    model = Ruang
    template_name = "satker/ruang_detail.html"
    context_object_name = 'ruang'


class RuangUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateRuangForm
    model = Ruang
    template_name = "satker/ruang_update.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:ruang_detail', kwargs={'pk': self.object.id_ruang})
        return success_url


class RuangDeleteView(LoginRequiredMixin, DeleteView):
    model = Ruang
    template_name = "satker/ruang_del_conf.html"
    success_url = reverse_lazy('satker:ruang_list')

    def dispatch(self, request, *args, **kwargs):
        ruang_obj = Ruang.objects.get(id_ruang=self.kwargs['pk'])
        if ruang_obj.is_used:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>(' + ruang_obj.nama +') Tidak dapat dihapus karena sudah digunakan.</h4>')
        return super().dispatch(request, *args, **kwargs)


class SatkerListView(LoginRequiredMixin, ListView):
    model = Satker
    template_name = "satker/satker_list.html"
    context_object_name = 'satker_list'
    ordering = ['id_satker']


class SatkerAddView(LoginRequiredMixin, CreateView):
    form_class = SatkerForm
    template_name = "satker/satker_add.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:detail', kwargs={'pk': self.object.id_satker})
        return success_url


class SatkerDetailView(LoginRequiredMixin, DetailView):
    model = Satker
    template_name = "satker/satker_detail.html"
    context_object_name = 'satker'


class SatkerUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateSatkerForm
    model = Satker
    template_name = "satker/satker_update.html"

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('satker:detail', kwargs={'pk': self.object.id_satker})
        return success_url


class SatkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Satker
    template_name = "satker/satker_del_conf.html"
    success_url = reverse_lazy('satker:list')

    def dispatch(self, request, *args, **kwargs):
        satker_obj = Satker.objects.get(id_satker=self.kwargs['pk'])
        if satker_obj.is_used:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>(' + satker_obj.nama +') Tidak dapat dihapus karena sudah digunakan.</h4>')
        return super().dispatch(request, *args, **kwargs)