from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
# Create your views here.
from .models import *
from inventory.models import Barang
from .form import PeminjamanForm, HabispakaiForm
from datetime import datetime
from reports.models import Mutasi

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

    def form_valid(self, form):
        # update user_updated
        form.instance.user_updated = user_updated(self)
        return super().form_valid(form)


class FormHabispakaiView(LoginRequiredMixin, CreateView):
    form_class = HabispakaiForm
    template_name = "transaksi/form_habispakai.html"

    def form_valid(self, form):
        # fill user_updated
        form.instance.user_updated = user_updated(self)
        # update jumlah barang
        id_b = str(form.cleaned_data['id_barang'])[0:7]
        jumlah = form.cleaned_data['jumlah']
        barang_obj = Barang.objects.get(id_barang=id_b)
        if jumlah == 0:
            messages.warning(self.request, 'Jumlah tidak boleh 0 !')
            return redirect(reverse('transaksi:form_habispakai'))
        else:
            barang_obj.jumlah = barang_obj.jumlah - jumlah
            barang_obj.save()
        # add mutasi obj
        mutasi_obj = Mutasi(
            id_barang = barang_obj,
            jenis = "Keluar",
            jumlah = jumlah,
            id_satker=barang_obj.id_tempat.id_ruang.id_satker,
            user_updated = user_updated(self),
            tgl_mutasi = barang_obj.tgl_pengadaan,
        )
        mutasi_obj.save()
        return super(FormHabispakaiView, self).form_valid(form)


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
