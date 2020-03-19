from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.conf import settings
import pytz
from .models import *
from .form import *
from datetime import datetime
from reports.models import Mutasi
from inventory.models import *


def user_updated(self):
    if self.request.user.get_full_name() == "":
        nama = self.request.user.username
    else:
        nama = self.request.user.get_full_name()
    return nama


class TransaksiListView(LoginRequiredMixin, ListView):
    model = Transaksi
    template_name = "transaksi/trans_list.html"
    context_object_name = 'transaksi_list'
    ordering = ['id_transaksi']


class TransDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaksi
    template_name = "transaksi/trans_delete_confirmation.html"
    success_url = reverse_lazy('transaksi:transaksi_list')

    def dispatch(self, request, *args, **kwargs):
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.kwargs['pk'])
        if transaksi_obj.tgl_pengambilan.month != datetime.now().month or transaksi_obj.tgl_pengambilan.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat menghapus transaksi yang tercatat pada tahun dan bulan saat ini!</h4>')
        return super().dispatch(request, *args, **kwargs)


class FormPeminjamanView(LoginRequiredMixin, CreateView):
    form_class = PeminjamanForm
    template_name = "transaksi/form_peminjaman.html"

    def get_success_url(self):
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.object.id_transaksi)
        transaksi_obj.transaksi = "Peminjaman"
        transaksi_obj.user_updated = user_updated(self)
        transaksi_obj.save()

        barang_obj = Barang.objects.get(id_barang=self.object.id_barang.id_barang)
        barang_obj.in_transaction = True
        barang_obj.save()
        messages.success(self.request, 'Transaksi disimpan.')
        success_url = reverse_lazy('transaksi:transaksi_detail', kwargs={
                                   'pk': self.object.id_transaksi})
        return success_url
        


class FormHabispakaiView(LoginRequiredMixin, CreateView):
    form_class = HabispakaiForm
    template_name = "transaksi/form_habispakai.html"

    def form_valid(self, form):
        self.form = form
        barang_obj = form.cleaned_data['id_barang']
        jumlah = form.cleaned_data['jumlah']
        pengguna = form.cleaned_data['pengguna']
        tgl_pengambilan = form.cleaned_data['tgl_pengambilan']

        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        try:
            mutasi_obj = Mutasi.objects.all().filter(id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tgl.year, tgl_mutasi__month=get_tgl.month).get(id_barang=barang_obj.id_barang)
            # update Barang obj
            barang_obj.jumlah_b = barang_obj.jumlah_b - jumlah
            barang_obj.in_transaction = True
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            # update Mutasi obj
            mutasi_obj.nama_barang = barang_obj.nama
            mutasi_obj.keluar = mutasi_obj.keluar + jumlah
            mutasi_obj.tgl_mutasi = tgl_pengambilan
            mutasi_obj.save()
        except Exception as err:
            # update Barang obj
            barang_obj.jumlah_b = barang_obj.jumlah_b - jumlah
            barang_obj.in_transaction = True
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            # create Mutasi obj
            tempat_obj = Tempat.objects.get(
                id_tempat=barang_obj.id_tempat.id_tempat)
            new_obj = Mutasi(
                id_barang=barang_obj.id_barang,
                nama_barang=barang_obj.nama,
                kategori= barang_obj.id_kategori.id_kategori,
                id_satker=tempat_obj.id_ruang.id_satker,
                tgl_mutasi=tgl_pengambilan,
                nilai_barang=barang_obj.nilai_barang,
                jumlah_awal=barang_obj.jumlah_b + jumlah,
                masuk=0,
                keluar=jumlah,
                user_updated=user_updated(self),
            )
            new_obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang.id_barang)
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.object.id_transaksi)
        transaksi_obj.transaksi = "Persediaan"
        transaksi_obj.satuan = barang_obj.satuan
        transaksi_obj.user_updated = user_updated(self)
        transaksi_obj.save()

        messages.success(self.request, 'Transaksi disimpan.')
        success_url = reverse_lazy('transaksi:transaksi_detail', kwargs={
                                   'pk': self.object.id_transaksi})
        return success_url


class TransaksiDetail(LoginRequiredMixin, DetailView):
    model = Transaksi
    template_name = "transaksi/trans_detail.html"
    context_object_name = 'transaksi'


class PeminjamanUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PeminjamanForm
    model = Transaksi
    template_name = "transaksi/form_update_peminjaman.html"

    def dispatch(self, request, *args, **kwargs):
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.kwargs['pk'])
        if transaksi_obj.tgl_pengambilan.month != datetime.now().month or transaksi_obj.tgl_pengambilan.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat mengedit transaksi yang tercatat pada tahun dan bulan saat ini!</h4>')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # update user_updated
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Transaksi diperbarui.')
        success_url = reverse_lazy('transaksi:transaksi_detail', kwargs={
                                   'pk': self.object.id_transaksi})
        return success_url


class HabisPakaiUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateHabispakaiForm
    model = Transaksi
    template_name = "transaksi/form_update_habispakai.html"

    def dispatch(self, request, *args, **kwargs):
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.kwargs['pk'])
        if transaksi_obj.tgl_pengambilan.month != datetime.now().month or transaksi_obj.tgl_pengambilan.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat mengedit transaksi yang tercatat pada tahun dan bulan saat ini!</h4>')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        barang_obj = form.cleaned_data['id_barang']
        jumlah = form.cleaned_data['jumlah']
        pengguna = form.cleaned_data['pengguna']
        tgl_pengambilan = form.cleaned_data['tgl_pengambilan']
        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        try:
            # update Barang obj
            barang_obj.jumlah_b = barang_obj.jumlah_b - (jumlah - self.object.jumlah)
            barang_obj.in_transaction = True
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
        except Exception as err:
            messages.error(self.request, 'Gagal update data barang, hubungi administrator untuk update manual.')

        try:
            # update Mutasi obj
            mutasi_obj = Mutasi.objects.all().filter(id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tgl.year, tgl_mutasi__month=get_tgl.month).get(id_barang=barang_obj.id_barang)
            mutasi_obj.id_barang = barang_obj.id_barang
            mutasi_obj.nama_barang = barang_obj.nama
            mutasi_obj.kategori = barang_obj.id_kategori.id_kategori
            mutasi_obj.id_satker = barang_obj.id_tempat.id_ruang.id_satker
            mutasi_obj.tgl_mutasi = tgl_pengambilan
            mutasi_obj.nilai_barang = barang_obj.nilai_barang
            mutasi_obj.jumlah_awal = mutasi_obj.jumlah_awal - (jumlah - self.object.jumlah)
            mutasi_obj.keluar = mutasi_obj.keluar + (jumlah - self.object.jumlah)
            mutasi_obj.user_updated=user_updated(self)
            mutasi_obj.save()
        except Exception as err:
            messages.error(self.request, 'Gagal update data mutasi, hubungi administrator untuk update manual.')
        return super().form_valid(form)

    def get_success_url(self):
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.object.id_transaksi)
        transaksi_obj.user_updated = user_updated(self)
        transaksi_obj.save()
        messages.success(self.request, 'Transaksi diperbarui.')
        success_url = reverse_lazy('transaksi:transaksi_detail', kwargs={
                                   'pk': self.object.id_transaksi})
        return success_url
    


class PengembalianView(LoginRequiredMixin, FormView):
    template_name = "transaksi/form_pengembalian.html"
    form_class = PengembalianForm

    def form_valid(self, form):
        self.form = form
        id_transaksi = form.cleaned_data['transaksi']
        tgl_kembali = form.cleaned_data['tgl_kembali']
        transaksi_obj = Transaksi.objects.get(id_transaksi=id_transaksi)
        transaksi_obj.tgl_kembali = tgl_kembali
        transaksi_obj.user_updated = user_updated(self)
        transaksi_obj.updated = datetime.now()
        transaksi_obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        id_transaksi = self.form.cleaned_data['transaksi']
        transaksi_obj = Transaksi.objects.get(id_transaksi=id_transaksi)
        if not self.success_url:
            messages.success(self.request, 'Transaksi diperbarui.')
            return (reverse_lazy('transaksi:transaksi_detail', kwargs={'pk': transaksi_obj.id_transaksi})) 
        return (reverse_lazy('transaksi:form_pengembalian'))  # success_url may be lazy
