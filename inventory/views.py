from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView, RedirectView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Barang, Tempat, Ruang, Satker, Kategori
from transaksi.models import Transaksi
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


def check_transaction(id_b):
    barang_obj = Barang.objects.get(id_barang=id_b)
    return barang_obj.in_transaction


'''class BarcodeView(RedirectView):
    pattern_name = 'detail'

    def get_redirect_url(self, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        EAN = barcode.get_barcode_class('ean8')
        ean = EAN(self.kwargs['pk'], writer=ImageWriter())
        fullname = ean.save(os.path.join(
            'static/media/barcodes/' + self.kwargs['pk']))
        return reverse_lazy('inventory:detail', kwargs={'pk': barang_obj.pk})
'''

class InvManageView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "inventory/inv_list.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']


class InvAddView(LoginRequiredMixin, CreateView):
    form_class = BarangForm
    template_name = "inventory/inv_add.html"

    def get_success_url(self):
        # update field "is_used" in kategori,tempat, ruang, satker
        kategori_obj = Kategori.objects.get(id_kategori=self.object.id_kategori.id_kategori)
        kategori_obj.is_used = True
        kategori_obj.save()
        tempat_obj = Tempat.objects.get(id_tempat=self.object.id_tempat.id_tempat)
        tempat_obj.is_used = True
        tempat_obj.save()
        ruang_obj = Ruang.objects.get(id_ruang=self.object.id_tempat.id_ruang.id_ruang)
        ruang_obj.is_used = True
        ruang_obj.save()
        satker_obj = Satker.objects.get(id_satker=self.object.id_tempat.id_ruang.id_satker.id_satker)
        satker_obj.is_used = True
        satker_obj.save()

        #generate barcode if jenis = inventaris
        if self.object.jenis == "Inventaris" or self.object.jenis == "Modal":
            EAN = barcode.get_barcode_class('ean8')
            ean = EAN(self.object.id_barang, writer=ImageWriter())
            ean.save(os.path.join('static/media/barcodes/' + self.object.id_barang))
            barcode_loc = "media/barcodes/" + self.object.id_barang + ".png"
            self.object.barcode = barcode_loc
            self.object.save()

        #save to mutasi if jenis = persediaan
        if self.object.jenis == "Persediaan":
            mutasi_obj = Mutasi(
                id_barang = self.object.id_barang,
                nama_barang = self.object.nama,
                kategori = self.object.id_kategori.id_kategori,
                id_satker = tempat_obj.id_ruang.id_satker,
                tgl_mutasi = self.object.tgl_pengadaan,
                nilai_barang = self.object.nilai_barang,
                jumlah_awal = 0,
                masuk = self.object.jumlah_b,
                keluar = 0,
                user_updated=user_updated(self),
            )
            mutasi_obj.save()


        # update barang obj
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.jumlah_rr = 0
        barang_obj.jumlah_rb = 0
        barang_obj.jumlah_hl = 0
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        if self.object.jenis == "Persediaan":
            messages.success(self.request, 'Data barang dan mutasi ditambahkan.')
        else:
            messages.success(self.request, 'Data barang ditambahkan.')
        success_url = reverse_lazy('inventory:barang_detail', kwargs={
                                   'pk': self.object.id_barang})
        return success_url


class InvUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateBarangForm
    model = Barang
    template_name = "inventory/inv_update.html"

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        self.old_amount = barang_obj.jumlah
        self.old_date = barang_obj.tgl_pengadaan
        self.old_id_barang = barang_obj.id_barang
        if check_transaction(self.kwargs['pk']):
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Barang sudah tercatat dalam transaksi</h4>')
        elif barang_obj.is_past_due:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat mengedit Barang yang tercatat pada tahun dan bulan ini!</h4>')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.jumlah_b = self.object.jumlah - barang_obj.jumlah_rr
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        
        if self.object.jenis == "Persediaan":
            try:
                mutasi_obj = Mutasi.objects.filter(id_barang=self.object.id_barang, tgl_mutasi__year=get_tgl.year, tgl_mutasi__month=get_tgl.month).get(id_barang=self.object.id_barang)
                mutasi_obj.nama_barang = self.object.nama
                mutasi_obj.kategori = self.object.id_kategori.id_kategori
                mutasi_obj.id_satker = self.object.id_tempat.id_ruang.id_satker
                mutasi_obj.tgl_mutasi = self.object.tgl_pengadaan
                mutasi_obj.nilai_barang = self.object.nilai_barang
                mutasi_obj.masuk = mutasi_obj.masuk - (self.old_amount - self.object.jumlah)
                mutasi_obj.user_updated = user_updated(self)
                mutasi_obj.save()
                messages.success(self.request, 'Data barang dan mutasi diperbarui.')
            except Exception as err:
                print(err)
                messages.error(self.request, 'Gagal update mutasi, hubungi administrator untuk update manual.')
        else:
            messages.success(self.request, 'Data barang diperbarui.')
        success_url = reverse_lazy('inventory:barang_detail', kwargs={
                                   'pk': self.object.id_barang})
        return success_url


class InvConditionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ConditionUpdateForm
    model = Barang
    template_name = "inventory/inv_condition_update.html"

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if barang_obj.jenis == "Persediaan":
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya barang Inventaris yang memiliki kondisi barang</h4>')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.in_transaction = True
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        messages.success(self.request, 'Kondisi barang diperbarui.')
        success_url = reverse_lazy('inventory:barang_detail', kwargs={
                                   'pk': self.object.id_barang})
        return success_url

    def get_context_data(self, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        total = barang_obj.jumlah_b + barang_obj.jumlah_rr + barang_obj.jumlah_rb + barang_obj.jumlah_hl
        self.kwargs.update({
            'total': total
            })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context
    


class InvDeleteView(LoginRequiredMixin, DeleteView):
    model = Barang
    template_name = "inventory/inv_delete_confirmation.html"
    success_url = reverse_lazy('inventory:manage')

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if check_transaction(self.kwargs['pk']):
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Barang sudah tercatat dalam transaksi</h4>')
        elif barang_obj.is_past_due:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat menghapus barang yang tercatat pada tahun dan bulan ini!</h4>')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        if self.object.jenis == "Persediaan":
            try:
                get_date = self.object.tgl_pengadaan
                mutasi_obj = Mutasi.objects.filter(id_barang=self.object.id_barang, tgl_mutasi__month=get_date.month, tgl_mutasi__year=get_date.year).get(id_barang=self.object.id_barang)
                mutasi_obj.delete()
            except Exception as err:
                messages.error(self.request, 'Gagal hapus mutasi, hubungi administrator untuk hapus manual.')
        success_url = reverse_lazy('inventory:barang_list')
        return success_url


class InvDetailView(LoginRequiredMixin, DetailView):
    model = Barang
    template_name = "inventory/inv_detail.html"
    context_object_name = 'barang'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        transaksi_obj = Transaksi.objects.all().filter(id_barang = self.object, tgl_kembali = None)
        context['Peminjaman'] = transaksi_obj
        context.update(kwargs)
        return super().get_context_data(**context)


class InvAddExisting(LoginRequiredMixin, FormView):
    template_name = "inventory/inv_add_existing.html"
    form_class = AddExistingForm

    def form_valid(self, form):
        self.form = form
        barang_obj = form.cleaned_data['id_barang']
        jumlah = form.cleaned_data['jumlah']

        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        try:
            mutasi_obj = Mutasi.objects.all().filter(id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tgl.year, tgl_mutasi__month=get_tgl.month).get(id_barang=barang_obj.id_barang)
            # update Barang obj
            barang_obj.jumlah_b = barang_obj.jumlah_b + jumlah
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            # update Mutasi obj
            mutasi_obj.masuk = mutasi_obj.masuk + jumlah
            mutasi_obj.user_updated=user_updated(self)
            mutasi_obj.save()
            messages.success(self.request, 'Data barang dan mutasi diperbarui.')
        except Exception as err:
            # update Barang obj
            barang_obj.jumlah_b = barang_obj.jumlah_b + jumlah
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            # create Mutasi obj
            tempat_obj = Tempat.objects.get(id_tempat=barang_obj.id_tempat.id_tempat)
            new_obj = Mutasi(
                id_barang=barang_obj.id_barang,
                nama_barang=barang_obj.nama,
                kategori = barang_obj.id_kategori.nama,
                id_satker=tempat_obj.id_ruang.id_satker,
                tgl_mutasi=get_tgl,
                nilai_barang=barang_obj.nilai_barang,
                jumlah_awal=barang_obj.jumlah_b - jumlah,
                masuk=jumlah,
                keluar=0,
                user_updated=user_updated(self),
            )
            new_obj.save()
            messages.success(self.request, 'Data barang diperbarui dan mutasi ditambahkan.')
            
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        barang_obj = self.form.cleaned_data['id_barang']
        if not self.success_url:
            return (reverse_lazy('inventory:barang_detail', kwargs={'pk': barang_obj.id_barang})) 
        return (reverse_lazy('inventory:add_existing_good'))  # success_url may be lazy


class KategoriListView(LoginRequiredMixin, ListView):
    model = Kategori
    template_name = "kategori/kategori_list.html"
    context_object_name = 'kategori_list'
    ordering = ['id_kategori']


class KategoriAddView(LoginRequiredMixin, CreateView):
    form_class = KategoriForm
    template_name = "kategori/kategori_add.html"

    def form_valid(self, form):
        form.instance.nama = form.instance.nama.upper()
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('inventory:kategori_list')
        return success_url


class KategoriUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateKategoriForm
    model = Kategori
    template_name = "kategori/kategori_update.html"
    
    def form_valid(self, form):
        # fill user_updated
        form.instance.nama = form.instance.nama.upper()
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object.user_updated = user_updated(self)
        self.object.save()
        success_url = reverse_lazy('inventory:kategori_list')
        return success_url


class KategoriDeleteView(LoginRequiredMixin, DeleteView):
    model = Kategori
    template_name = "kategori/kategori_del_conf.html"
    success_url = reverse_lazy('inventory:kategori_list')

    def dispatch(self, request, *args, **kwargs):
        kategori_obj = Kategori.objects.get(id_kategori=self.kwargs['pk'])
        if kategori_obj.is_used:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>(' + kategori_obj.nama +') Tidak dapat dihapus karena sudah digunakan.</h4>')
        return super().dispatch(request, *args, **kwargs)


class BarcodePrintView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/barcode_print.html"

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if barang_obj.jenis != "Inventaris" and barang_obj.jenis != "Modal":
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Cetak barcode hanya untuk barang inventaris atau Modal.</h4>')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        dict = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei",
            6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober",
            11: "November", 12: "Desember",
        }
        get_day = barang_obj.tgl_pengadaan.day
        get_month = barang_obj.tgl_pengadaan.month
        get_year = barang_obj.tgl_pengadaan.year
        self.kwargs.update({
            'satker': barang_obj.id_tempat.id_ruang.id_satker.nama.upper(),
            'nama': barang_obj.nama.upper(),
            'id_barang': barang_obj.id_barang,
            'tgl_pengadaan': str(get_day) + ' ' + dict[get_month].upper() + ' ' + str(get_year),
            'barcode': barang_obj.barcode,
            })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context