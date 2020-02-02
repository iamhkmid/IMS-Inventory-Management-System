from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Barang, Tempat, Ruang, Satker, auto_id_barang
from .form import BarangForm, SatkerForm, RuangForm, TempatForm
from datetime import datetime
from reports.models import Mutasi
from django.utils.dateparse import parse_datetime
from django.conf import settings
import pytz


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
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            parse_tgl = parse_datetime(request.POST['tgl_pengadaan'])
            get_tgl = parse_tgl.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            #cek bulan dan tahun
            if get_tgl.month == datetime.now().month:
                try:
                    nama_b = request.POST.get('nama')
                    barang_obj = Barang.objects.get(nama=nama_b)
                except Exception as err:
                    #jika nama barang blm ada
                    return super().post(request, *args, **kwargs)
                #jika nama sudah ada
                messages.warning(request, 'Nama Barang Sudah Ada !')
            #jika bulan dan tahun tidak sama
            else:
                messages.warning(request, 'Penambahan harus pada bulan ini !')
        return redirect('inventory:add')

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # add Mutasi obj
        tempat_obj = Tempat.objects.get(
            id_tempat=self.object.id_tempat.id_tempat)
        mutasi_obj = Mutasi(
            id_barang = self.object.id_barang,
            nama_barang = self.object.nama,
            id_satker = tempat_obj.id_ruang.id_satker,
            tgl_mutasi = self.object.tgl_pengadaan,
            nilai_barang = self.object.nilai_barang,
            jumlah_awal = 0,
            masuk = self.object.jumlah,
            keluar = 0,
            user_updated = user_updated(self),
        )
        mutasi_obj.save()
        success_url = reverse_lazy('inventory:detail', kwargs={
                                   'slug': self.object.id_barang})
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


class InvAddExisting(TemplateView):
    template_name = "inventory/inv_add_exiting.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            id_barang = request.POST['id_barang']
            barang_obj = Barang.objects.get(id_barang=id_barang)
            
            jumlah = request.POST['jumlah']
            tgl = request.POST['tgl_pengadaan']
            parse_tgl = parse_datetime(request.POST['tgl_pengadaan'])
            get_tgl = parse_tgl.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            get_bulan = tgl[5:7]
            get_tahun = tgl[0:4]
            # cek tgl penambahan
            if get_tgl.month == datetime.now().month:
                try:
                    #filter bulan dan tahun
                    mutasi_filter = Mutasi.objects.filter(id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tahun, tgl_mutasi__month=get_bulan)
                    mutasi_obj = mutasi_filter.get(id_barang=barang_obj.id_barang)
                    if mutasi_obj.id_barang == barang_obj.id_barang:
                        #update Barang obj
                        barang_obj.jumlah = barang_obj.jumlah + int(jumlah)
                        barang_obj.user_updated = user_updated(self)
                        barang_obj.save()
                        # update Mutasi obj
                        mutasi_obj.nama_barang = barang_obj.nama
                        mutasi_obj.masuk = mutasi_obj.masuk + int(jumlah)
                        mutasi_obj.tgl_mutasi = get_tgl
                        mutasi_obj.save()
                        #jika ditemukan mutasi pada bulan dan tahun yang sama
                        return redirect('inventory:detail', id_barang)
                    
                except Exception as err:
                    #update Barang obj
                    barang_obj.jumlah = barang_obj.jumlah + int(jumlah)
                    barang_obj.updated = datetime.now()
                    barang_obj.user_updated = user_updated(self)
                    barang_obj.save()
                    #create Mutasi obj
                    tempat_obj = Tempat.objects.get(id_tempat=barang_obj.id_tempat.id_tempat)
                    mutasi_obj = Mutasi(
                        id_barang = barang_obj.id_barang,
                        nama_barang = barang_obj.nama,
                        id_satker = tempat_obj.id_ruang.id_satker,
                        tgl_mutasi = get_tgl,
                        nilai_barang = barang_obj.nilai_barang,
                        jumlah_awal = barang_obj.jumlah - int(jumlah),
                        masuk = jumlah,
                        keluar = 0,
                        user_updated = user_updated(self),
                    )
                    mutasi_obj.save()
                    return redirect('inventory:detail', id_barang)
            else:
                messages.warning(request, 'Penambahan harus pada bulan ini !')
            
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        barang_list = Barang.objects.values_list('id_barang', 'nama')
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

    
class TempatUpdateView(UpdateView):
    form_class = TempatForm
    model = Tempat
    template_name = "tempat/tempat_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class TempatUpdateView(UpdateView):
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

    
class RuangUpdateView(UpdateView):
    form_class = RuangForm
    model = Ruang
    template_name = "tempat/ruang_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class RuangUpdateView(UpdateView):
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

    
class SatkerUpdateView(UpdateView):
    form_class = SatkerForm
    model = Satker
    template_name = "satker/satker_update.html"

    def form_valid(self, form):
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class SatkerUpdateView(UpdateView):
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