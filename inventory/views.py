from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Barang, Tempat, Ruang, Satker, auto_id_barang
from .form import BarangForm
from datetime import datetime
from reports.models import Mutasi


def user_updated(self):
    if self.request.user.get_full_name() == "":
        nama = self.request.user.username
    else:
        nama = self.request.user.get_full_name()
    return nama

class InvManageView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "inventory/inv_manage.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']


class InvAddView(LoginRequiredMixin, CreateView):
    form_class = BarangForm
    template_name = "inventory/inv_add.html"

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        self.object = form.save()        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        # add Mutasi obj
        tempat_obj = Tempat.objects.get(id_tempat=self.object.id_tempat.id_tempat)
        mutasi_obj = Mutasi(
            id_barang = self.object,
            jenis = "Masuk",
            jumlah = self.object.jumlah,
            id_satker = tempat_obj.id_ruang.id_satker,
            user_updated = user_updated(self),
            tgl_mutasi = self.object.tgl_pengadaan,
        )
        mutasi_obj.save()
        success_url = reverse_lazy('inventory:detail', kwargs = {'slug': self.object.id_barang})
        return success_url


class InvUpdateView(UpdateView):
    form_class = BarangForm
    model = Barang
    template_name = "inventory/inv_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class InvDeleteView(LoginRequiredMixin, DeleteView):
    model = Barang
    template_name = "inventory/inv_delete_confirmation.html"
    success_url = reverse_lazy('inventory:manage')


class InvDetailView(LoginRequiredMixin, DetailView):
    model = Barang
    template_name = "inventory/inv_detail.html"
    context_object_name = 'barang'


class TempatListView(LoginRequiredMixin, ListView):
    model = Tempat
    template_name = "tempat/tempat_list.html"
    context_object_name = 'tempat_list'
    ordering = ['id_tempat']


class RuangListView(LoginRequiredMixin, ListView):
    model = Ruang
    template_name = "tempat/ruang_list.html"
    context_object_name = 'ruang_list'
    ordering = ['id_ruang']


class SatkerListView(LoginRequiredMixin, ListView):
    model = Satker
    template_name = "tempat/satker_list.html"
    context_object_name = 'satker_list'
    ordering = ['id_satker']


class InvAddExisting(TemplateView):
    template_name = "inventory/inv_add_exiting.html"

    def post(self, request,*args, **kwargs):
        if request.method == "POST":
            id_barang = request.POST['id_barang']
            jumlah = request.POST['jumlah']
            # update obj Barang
            barang_obj = Barang.objects.get(id_barang=id_barang)
            barang_obj.jumlah = barang_obj.jumlah + int(jumlah)
            barang_obj.updated = datetime.now()
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            # add Mutasi obj
            tempat_obj = Tempat.objects.get(id_tempat=barang_obj.id_tempat.id_tempat)
            mutasi_obj = Mutasi(
                id_barang = barang_obj,
                jenis = "Masuk",
                jumlah = jumlah,
                id_satker = tempat_obj.id_ruang.id_satker,
                user_updated = user_updated(self),
                tgl_mutasi = barang_obj.tgl_pengadaan,
            )
            mutasi_obj.save()
            return redirect('inventory:detail', id_barang)
        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        barang_list = Barang.objects.values_list('id_barang', 'nama')
        self.kwargs.update({'barang_list': barang_list})
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context
