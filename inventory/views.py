from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView, RedirectView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Barang, Tempat, Ruang, Satker, Kategori
from .form import BarangForm, SatkerForm, RuangForm, TempatForm, ConditionUpdateForm, KategoriForm
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
        return reverse_lazy('inventory:detail', kwargs={'slug': barang_obj.slug})
'''

class InvManageView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "inventory/inv_manage.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']


class InvAddView(LoginRequiredMixin, CreateView):
    form_class = BarangForm
    template_name = "inventory/inv_add.html"

    def post(self, request, *args, **kwargs):
        input_valid = True
        if request.method == 'POST':
            parse_tgl = parse_datetime(request.POST['tgl_pengadaan'])
            get_tgl = parse_tgl.replace(
                tzinfo=pytz.timezone(settings.TIME_ZONE))
            nama_b = request.POST.get('nama')
            id_b = request.POST.get('id_barang')
            mutasi_list = Barang.objects.values_list('id_barang','nama')
            for v_id, v_nama in mutasi_list:
                if v_id == id_b:
                    input_valid = False
                    messages.warning(request, 'ID Barang Sudah Ada !')
                if v_nama == nama_b:
                    input_valid = False
                    messages.warning(request, 'Nama Barang Sudah Ada !')
            if get_tgl.month != datetime.now().month or get_tgl.year != datetime.now().year:
                input_valid = False
                messages.warning(request, 'Penambahan harus pada tahun dan bulan saat ini !')
        if input_valid:
            return super().post(request, *args, **kwargs)
        return redirect('inventory:add')
        

    def get_success_url(self):
        if self.object.jenis == "Inventaris":
            EAN = barcode.get_barcode_class('ean8')
            ean = EAN(self.object.id_barang, writer=ImageWriter())
            ean.save(os.path.join('static/media/barcodes/' + self.object.id_barang))
            barcode_loc = "media/barcodes/" + self.object.id_barang + ".png"
            self.object.barcode = barcode_loc
            self.object.save()

        # add Mutasi obj
        tempat_obj = Tempat.objects.get(
            id_tempat=self.object.id_tempat.id_tempat)

        
        if self.object.jenis == "Persediaan":
            mutasi_obj = Mutasi(
                id_barang = self.object.id_barang,
                nama_barang = self.object.nama,
                kategori = self.object.id_kategori.nama,
                id_satker = tempat_obj.id_ruang.id_satker,
                tgl_mutasi = self.object.tgl_pengadaan,
                nilai_barang = self.object.nilai_barang,
                jumlah_awal = 0,
                masuk = self.object.jumlah,
                keluar = 0,
                user_updated=user_updated(self),
            )
            mutasi_obj.save()
        # save user_updated
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.jumlah_b = self.object.jumlah
        barang_obj.jumlah_rr = 0
        barang_obj.jumlah_rb = 0
        barang_obj.jumlah_hl = 0
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        success_url = reverse_lazy('inventory:detail', kwargs={
                                   'slug': self.object.id_barang})
        return success_url


class InvUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BarangForm
    model = Barang
    template_name = "inventory/inv_update.html"


    def post(self, request, *args, **kwargs):
        input_valid = True
        if request.method == 'POST':
            parse_tgl = parse_datetime(request.POST['tgl_pengadaan'])
            get_tgl = parse_tgl.replace(
                tzinfo=pytz.timezone(settings.TIME_ZONE))
            if get_tgl.month != datetime.now().month or get_tgl.year != datetime.now().year:
                input_valid = False
                messages.warning(request, 'Update harus pada tahun dan bulan saat ini !')
        if input_valid:
            return super().post(request, *args, **kwargs)
        return redirect('inventory:update', self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if check_transaction(self.kwargs['pk']):
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Barang sudah tercatat dalam transaksi</h4>')
        elif barang_obj.tgl_pengadaan.month != datetime.now().month or barang_obj.tgl_pengadaan.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat mengedit Barang yang tercatat pada tahun dan bulan ini!</h4>')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        success_url = reverse_lazy('inventory:detail', kwargs={
                                   'slug': self.object.id_barang})
        return success_url


class InvConditionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ConditionUpdateForm
    model = Barang
    template_name = "inventory/inv_condition_update.html"

    def post(self, request, *args, **kwargs):
        input_valid = True
        if request.method == 'POST':
            barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
            barang_obj.in_transaction = True
            barang_obj.user_updated = user_updated(self)
            barang_obj.save()
            jumlah = barang_obj.jumlah
            jumlah_b = int(request.POST.get('jumlah_b'))
            jumlah_rr = int(request.POST.get('jumlah_rr'))
            jumlah_rb = int(request.POST.get('jumlah_rb'))
            jumlah_hl = int(request.POST.get('jumlah_hl'))
            total = jumlah_b + jumlah_rr + jumlah_rb + jumlah_hl
            if jumlah != total:
                input_valid = False
                messages.warning(request, 'Total Kondisi Barang tidak sesuai dengan jumlah barang!')
        if input_valid:
            return super().post(request, *args, **kwargs)
        return redirect('inventory:condition_update', self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if barang_obj.jenis == "Persediaan":
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya barang Inventaris yang memiliki kondisi barang</h4>')
        elif barang_obj.tgl_pengadaan.month != datetime.now().month or barang_obj.tgl_pengadaan.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat mengedit kondisi barang yang tercatat pada tahun dan bulan ini!</h4>')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang)
        barang_obj.user_updated = user_updated(self)
        barang_obj.save()
        success_url = reverse_lazy('inventory:detail', kwargs={
                                   'slug': self.object.id_barang})
        return success_url


class InvDeleteView(LoginRequiredMixin, DeleteView):
    model = Barang
    template_name = "inventory/inv_delete_confirmation.html"
    success_url = reverse_lazy('inventory:manage')

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        get_date = barang_obj.tgl_pengadaan
        if check_transaction(self.kwargs['pk']):
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Barang sudah tercatat dalam transaksi</h4>')
        elif get_date.month != datetime.now().month or get_date.year != datetime.now().year:
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Hanya dapat menghapus barang yang tercatat pada tahun dan bulan ini!</h4>')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        try:
            get_date = self.object.tgl_pengadaan
            mutasi_obj = Mutasi.objects.filter(id_barang=self.object.id_barang, tgl_mutasi__month=get_date.month, tgl_mutasi__year=get_date.year).get(id_barang=self.object.id_barang)
            mutasi_obj.delete()
        except Exception as err:
            pass
        success_url = reverse_lazy('inventory:manage')
        return success_url


class InvDetailView(LoginRequiredMixin, DetailView):
    model = Barang
    template_name = "inventory/inv_detail.html"
    context_object_name = 'barang'


class InvAddExisting(LoginRequiredMixin, TemplateView):
    template_name = "inventory/inv_add_existing.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            id_barang = request.POST['id_barang']
            barang_obj = Barang.objects.get(id_barang=id_barang)
            jumlah = request.POST['jumlah']
            get_tgl = datetime.now()
            # cek tgl penambahan
            try:
                # filter bulan dan tahun
                mutasi_filter = Mutasi.objects.filter(
                    id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tgl.year, tgl_mutasi__month=get_tgl.month)
                mutasi_obj = mutasi_filter.get(
                    id_barang=barang_obj.id_barang)
                if mutasi_obj.id_barang == barang_obj.id_barang:
                    # update Barang obj
                    barang_obj.jumlah = barang_obj.jumlah + int(jumlah)
                    barang_obj.user_updated = user_updated(self)
                    barang_obj.save()
                    # update Mutasi obj
                    mutasi_obj.nama_barang = barang_obj.nama
                    mutasi_obj.masuk = mutasi_obj.masuk + int(jumlah)
                    mutasi_obj.tgl_mutasi = get_tgl
                    mutasi_obj.save()
                    # jika ditemukan mutasi pada bulan dan tahun yang sama
                    return redirect('inventory:detail', id_barang)

            except Exception as err:
                # update Barang obj
                barang_obj.jumlah = barang_obj.jumlah + int(jumlah)
                barang_obj.updated = datetime.now()
                barang_obj.user_updated = user_updated(self)
                barang_obj.save()
                # create Mutasi obj
                tempat_obj = Tempat.objects.get(
                    id_tempat=barang_obj.id_tempat.id_tempat)
                mutasi_obj = Mutasi(
                    id_barang=barang_obj.id_barang,
                    nama_barang=barang_obj.nama,
                    kategori = barang_obj.id_kategori.nama,
                    id_satker=tempat_obj.id_ruang.id_satker,
                    tgl_mutasi=get_tgl,
                    nilai_barang=barang_obj.nilai_barang,
                    jumlah_awal=barang_obj.jumlah - int(jumlah),
                    masuk=jumlah,
                    keluar=0,
                    user_updated=user_updated(self),
                )
                mutasi_obj.save()
                return redirect('inventory:detail', id_barang)
            else:
                messages.warning(request, 'Penambahan harus pada bulan ini !')
        return redirect('inventory:add_existing_good')

    def get_context_data(self, **kwargs):
        barang_list = Barang.objects.filter(jenis="Persediaan").values_list('id_barang', 'nama')
        self.kwargs.update({'barang_list': barang_list})
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class TempatListView(LoginRequiredMixin, ListView):
    model = Tempat
    template_name = "tempat/tempat_list.html"
    context_object_name = 'tempat_list'
    ordering = ['id_tempat']


class TempatAddView(LoginRequiredMixin, CreateView):
    form_class = TempatForm
    template_name = "tempat/tempat_add.html"

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class TempatDetailView(LoginRequiredMixin, DetailView):
    model = Tempat
    template_name = "tempat/tempat_detail.html"
    context_object_name = 'tempat'


class TempatUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TempatForm
    model = Tempat
    template_name = "tempat/tempat_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)



class TempatDeleteView(LoginRequiredMixin, DeleteView):
    model = Tempat
    template_name = "tempat/tempat_del_conf.html"
    success_url = reverse_lazy('inventory:tempat_list')


class RuangListView(LoginRequiredMixin, ListView):
    model = Ruang
    template_name = "tempat/ruang_list.html"
    context_object_name = 'ruang_list'
    ordering = ['id_ruang']


class RuangAddView(LoginRequiredMixin, CreateView):
    form_class = RuangForm
    template_name = "tempat/ruang_add.html"

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class RuangDetailView(LoginRequiredMixin, DetailView):
    model = Ruang
    template_name = "tempat/ruang_detail.html"
    context_object_name = 'ruang'


class RuangUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RuangForm
    model = Ruang
    template_name = "tempat/ruang_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)




class RuangDeleteView(LoginRequiredMixin, DeleteView):
    model = Ruang
    template_name = "tempat/ruang_del_conf.html"
    success_url = reverse_lazy('inventory:ruang_list')


class SatkerListView(LoginRequiredMixin, ListView):
    model = Satker
    template_name = "tempat/satker_list.html"
    context_object_name = 'satker_list'
    ordering = ['id_satker']


class SatkerAddView(LoginRequiredMixin, CreateView):
    form_class = SatkerForm
    template_name = "tempat/satker_add.html"

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class SatkerDetailView(LoginRequiredMixin, DetailView):
    model = Satker
    template_name = "tempat/satker_detail.html"
    context_object_name = 'satker'


class SatkerUpdateView(LoginRequiredMixin, UpdateView):
    form_class = SatkerForm
    model = Satker
    template_name = "tempat/satker_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)



class SatkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Satker
    template_name = "tempat/satker_del_conf.html"
    success_url = reverse_lazy('inventory:satker_list')


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
    form_class = KategoriForm
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


class BarcodePrintView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/barcode_print.html"

    def dispatch(self, request, *args, **kwargs):
        barang_obj = Barang.objects.get(id_barang=self.kwargs['pk'])
        if barang_obj.jenis != "Inventaris":
            return HttpResponseNotFound('<h1>Access denied</h1><h4>Cetak barcode hanya untuk barang inventaris !</h4>')
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