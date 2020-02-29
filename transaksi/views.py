from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.conf import settings
import pytz
from .models import *
from .form import PeminjamanForm, HabispakaiForm
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
    success_url = reverse_lazy('transaksi:list')


class FormPeminjamanView(LoginRequiredMixin, CreateView):
    form_class = PeminjamanForm
    template_name = "transaksi/form_peminjaman.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            id_barang = request.POST['id_barang']
            barang_obj = Barang.objects.get(id_barang=id_barang)
            jumlah = request.POST['jumlah']
            tot = barang_obj.jumlah- int(jumlah)
            if  tot <= 0:
                    messages.warning(request, 'Barang Tidak Mencukupi !')
            else:
                return super().post(request, *args, **kwargs)
        return redirect('transaksi:form_peminjaman')

    def form_valid(self, form):
        # update user_updated
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)

    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang.id_barang)
        barang_obj.in_transaction = True
        barang_obj.save()
        success_url = reverse_lazy('transaksi:detail', kwargs={
                                   'slug': self.object.id_transaksi})
        return success_url


class FormHabispakaiView(LoginRequiredMixin, CreateView):
    form_class = HabispakaiForm
    template_name = "transaksi/form_habispakai.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            id_barang = request.POST['id_barang']
            barang_obj = Barang.objects.get(id_barang=id_barang)
            jumlah = request.POST['jumlah']
            tgl = request.POST['tgl_pengambilan']
            parse_tgl = parse_datetime(tgl)
            get_tgl = parse_tgl.replace(
                tzinfo=pytz.timezone(settings.TIME_ZONE))
            get_bulan = tgl[5:7]
            get_tahun = tgl[0:4]
            tot = barang_obj.jumlah- int(jumlah)
            # cek bulan dan tahun
            if get_tgl.month == datetime.now().month:
                if  tot <= 0:
                    messages.warning(request, 'Barang Tidak Mencukupi !')
                else:
                    try:
                        # filter bulan dan tahun
                        mutasi_filter = Mutasi.objects.filter(
                            id_barang=barang_obj.id_barang, tgl_mutasi__year=get_tahun, tgl_mutasi__month=get_bulan)
                        mutasi_obj = mutasi_filter.get(
                            id_barang=barang_obj.id_barang)
                        if mutasi_obj.id_barang == barang_obj.id_barang:
                            # update Barang obj
                            barang_obj.jumlah = barang_obj.jumlah - int(jumlah)
                            barang_obj.user_updated = user_updated(self)
                            barang_obj.save()
                            # update Mutasi obj
                            mutasi_obj.nama_barang = barang_obj.nama
                            mutasi_obj.keluar = mutasi_obj.keluar + int(jumlah)
                            mutasi_obj.tgl_mutasi = get_tgl
                            mutasi_obj.save()
                            # jika ditemukan mutasi pada bulan dan tahun yang sama
                            return super().post(request, *args, **kwargs)

                    except Exception as err:
                        # update Barang obj
                        barang_obj.jumlah = barang_obj.jumlah - int(jumlah)
                        barang_obj.user_updated = user_updated(self)
                        barang_obj.save()
                        # create Mutasi obj
                        tempat_obj = Tempat.objects.get(
                            id_tempat=barang_obj.id_tempat.id_tempat)
                        mutasi_obj = Mutasi(
                            id_barang=barang_obj.id_barang,
                            nama_barang=barang_obj.nama,
                            id_satker=tempat_obj.id_ruang.id_satker,
                            tgl_mutasi=get_tgl,
                            nilai_barang=barang_obj.nilai_barang,
                            jumlah_awal=barang_obj.jumlah + int(jumlah),
                            masuk=0,
                            keluar=jumlah,
                            user_updated=user_updated(self),
                        )
                        mutasi_obj.save()
                        return super().post(request, *args, **kwargs)
            else:
                messages.warning(request, 'Transaksi harus pada bulan ini !')
        return redirect('transaksi:form_habispakai')

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        return super(FormHabispakaiView, self).form_valid(form)
    
    def get_success_url(self):
        barang_obj = Barang.objects.get(id_barang=self.object.id_barang.id_barang)
        barang_obj.in_transaction = True
        barang_obj.save()
        success_url = reverse_lazy('transaksi:detail', kwargs={
                                   'slug': self.object.id_transaksi})
        return success_url


class TransDetail(LoginRequiredMixin, DetailView):
    model = Transaksi
    template_name = "transaksi/trans_detail.html"
    context_object_name = 'transaksi'


class PeminjamanUpdateView(UpdateView):
    form_class = PeminjamanForm
    model = Transaksi
    template_name = "transaksi/form_update_peminjaman.html"

    def form_valid(self, form):
        # update user_updated
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class PersediaanUpdateView(UpdateView):
    form_class = HabispakaiForm
    model = Transaksi
    template_name = "transaksi/form_update_habispakai.html"

    def form_valid(self, form):
        # update user_updated
        form.instance.user_updated = user_updated(self)
        # update stok di barang
        id_b = str(form.cleaned_data['id_barang'])[0:7]
        jumlah = form.cleaned_data['jumlah']
        trans = Transaksi.objects.get(id_transaksi=self.object.id_transaksi)
        str_id = self.object.id_transaksi
        barang_obj = Barang.objects.get(id_barang=id_b)
        barang_obj.jumlah = barang_obj.jumlah + (trans.jumlah - jumlah)
        if jumlah == trans.jumlah:
            messages.warning(self.request, 'Jumlah sama dengan sebelumnya !')
            return redirect(reverse('transaksi:update2', kwargs={"pk": str_id}))
        else:
            if barang_obj.jumlah <= 0:
                messages.warning(self.request, 'Stok Habis atau Kurang!')
                form.instance.jumlah = trans.jumlah
                return redirect(reverse('transaksi:update2', kwargs={"pk": str_id}))
            else:
                barang_obj.save()
        return super().form_valid(form)


class PengembalianView(TemplateView):
    template_name = "transaksi/form_pengembalian.html"

    def post(self, request, *args, **kwargs):
        # update transaksi -> tgl_kembali
        if request.method == "POST":
            id_transaksi = request.POST['transaksi']
            tgl_kembali = request.POST['tgl_kembali']
            # update obj Barang
            transaksi_obj = Transaksi.objects.get(id_transaksi=id_transaksi)
            transaksi_obj.tgl_kembali = tgl_kembali
            transaksi_obj.user_updated = user_updated(self)
            transaksi_obj.updated = datetime.now()
            transaksi_obj.save()
            return redirect('transaksi:list')
        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        transaksi_list = Transaksi.objects.values_list(
            'pengguna', 'id_transaksi', 'id_barang__nama').filter(transaksi='Peminjaman')
        self.kwargs.update({'transaksi_list': transaksi_list})
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context
