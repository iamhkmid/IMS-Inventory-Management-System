from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from transaksi.models import Transaksi
from inventory.models import Satker
from .models import Mutasi
import calendar


class ReportsPeminjamanView(LoginRequiredMixin, ListView):
    model = Transaksi
    template_name = "reports/report_peminjaman.html"
    context_object_name = 'transaksi_list'
    ordering = ['id_transaksi']

    def get_queryset(self):
        # filter peminjaman
        get_satker = self.request.session['satker']
        get_tgl = self.request.session['tgl_report']
        get_bulan = get_tgl[5:7]
        get_tahun = get_tgl[0:4]
        get_transaksi = self.request.session['transaksi']
        self.queryset = self.model.objects.filter(tgl_pengambilan__year=get_tahun, tgl_pengambilan__month=get_bulan,
                                                  transaksi=get_transaksi, id_barang__id_tempat__id_ruang__id_satker=get_satker)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        get_satker = self.request.session['satker']
        get_tgl = self.request.session['tgl_report']
        get_bulan = get_tgl[5:7]
        get_tahun = get_tgl[0:4]
        get_transaksi = self.request.session['transaksi']
        dict = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April", "05": "Mei",
            "06": "Juni", "07": "Juli", "08": "Agustus", "09": "September", "10": "Oktober",
            "11": "November", "12": "Desember",
        }
        lastday = calendar.monthrange(int(get_tahun), int(get_bulan))[1]
        self.kwargs.update({
            'satker': get_satker,
            'date_report': str(lastday) + ' ' + dict[get_bulan].upper() + ' ' + get_tahun,
            'transaksi': get_transaksi,
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class ReportsPersediaanView(LoginRequiredMixin, ListView):
    model = Mutasi
    template_name = "reports/report_persediaan.html"
    context_object_name = 'mutasi_list'
    ordering = ['id_mutasi']

    def get_queryset(self):
        # filter peminjaman
        get_satker = self.request.session['satker']
        get_tgl = self.request.session['tgl_report']
        get_bulan = get_tgl[5:7]
        get_tahun = get_tgl[0:4]
        get_transaksi = self.request.session['transaksi']
        self.queryset = self.model.objects.filter(
            tgl_mutasi__year=get_tahun, tgl_mutasi__month=get_bulan, id_satker=get_satker)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        get_satker = self.request.session['satker']
        satker_obj = Satker.objects.get(id_satker=get_satker)
        get_tgl = self.request.session['tgl_report']
        get_bulan = get_tgl[5:7]
        get_tahun = get_tgl[0:4]
        get_transaksi = self.request.session['transaksi']
        dict = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April", "05": "Mei",
            "06": "Juni", "07": "Juli", "08": "Agustus", "09": "September", "10": "Oktober",
            "11": "November", "12": "Desember",
        }
        lastday = calendar.monthrange(int(get_tahun), int(get_bulan))[1]
        self.kwargs.update({
            'satker': satker_obj.nama,
            'date_report': str(lastday) + ' ' + dict[get_bulan].upper() + ' ' + get_tahun,
            'transaksi': get_transaksi,
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class ChooseReportsView(LoginRequiredMixin, TemplateView):
    template_name = "reports/choose_report.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            self.request.session['satker'] = request.POST['satker']
            self.request.session['transaksi'] = request.POST['transaksi']
            self.request.session['tgl_report'] = request.POST['tgl_report']
            if request.POST['transaksi'] == "Peminjaman":
                report_url = 'report:peminjaman'
            elif request.POST['transaksi'] == "Persediaan":
                report_url = "report:persediaan"
            return redirect(report_url)
        return render(request,  self.template_name)

    def get_context_data(self, **kwargs):
        satker_list = Satker.objects.values_list('id_satker', 'nama').distinct()
        self.kwargs.update({'satker_list': satker_list})
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class MutasiListView(LoginRequiredMixin, ListView):
    model = Mutasi
    template_name = "report/mutasi_list.html"
    context_object_name = 'mutasi_list'
    ordering = ['id_mutasi']
