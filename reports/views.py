from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from transaksi.models import Transaksi
from inventory.models import Satker
from .models import Mutasi
from inventory.models import Barang
import calendar
from dateutil import relativedelta
from django.utils.dateparse import parse_datetime, parse_date
from django.conf import settings
import pytz
from datetime import datetime

class ReportsInventarisView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "reports/report_inventaris.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

    def get_queryset(self):
        self.queryset = self.model.objects.filter(jenis=self.request.session['report_type'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        get_report_type = self.request.session['report_type']
        get_satker = self.request.session['satker']
        satker_obj = Satker.objects.get(id_satker=get_satker)
        dict = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei",
            6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober",
            11: "November", 12: "Desember",
        }
        get_day = datetime.now().day
        get_month = datetime.now().month
        get_year = datetime.now().year

        ruang_list = Barang.objects.filter(jenis="Inventaris").values_list("id_tempat","id_tempat__id_ruang__nama").distinct()

        self.kwargs.update({
            'get_satker': satker_obj.nama.upper(),
            'date_report': str(get_day) + ' ' + dict[get_month].upper() + ' ' + str(get_year),
            'report_type': get_report_type,
            'ruang_list': ruang_list,
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class ReportsPeminjamanView(LoginRequiredMixin, ListView):
    model = Transaksi
    template_name = "reports/report_peminjaman.html"
    context_object_name = 'transaksi_list'
    ordering = ['id_transaksi']

    def get_queryset(self):
        # filter peminjaman
        get_satker = self.request.session['satker']
        get_str_date = self.request.session['tgl_report']
        get_month = get_str_date[5:7]
        get_year = get_str_date[0:4]
        get_report_type = self.request.session['report_type']
        self.queryset = self.model.objects.filter(tgl_pengambilan__year=get_year, tgl_pengambilan__month=get_month,
                                                  transaksi=get_report_type, id_barang__id_tempat__id_ruang__id_satker=get_satker)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        get_report_type = self.request.session['report_type']
        get_satker = self.request.session['satker']
        satker_obj = Satker.objects.get(id_satker=get_satker)
        get_str_date = self.request.session['tgl_report']
        get_month = get_str_date[5:7]
        get_year = get_str_date[0:4]
        dict = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April", "05": "Mei",
            "06": "Juni", "07": "Juli", "08": "Agustus", "09": "September", "10": "Oktober",
            "11": "November", "12": "Desember",
        }
        lastday = calendar.monthrange(int(get_year), int(get_month))[1]
        self.kwargs.update({
            'get_satker': satker_obj.nama,
            'date_report': "1 - " + str(lastday) + ' ' + dict[get_month].upper() + ' ' + get_year,
            'report_type': get_report_type,
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
        get_str_date = self.request.session['tgl_report']
        get_month = get_str_date[5:7]
        get_year = get_str_date[0:4]
        self.queryset = self.model.objects.filter(
            tgl_mutasi__year=get_year, tgl_mutasi__month=get_month, id_satker=get_satker)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        get_report_type = self.request.session['report_type']
        get_satker = self.request.session['satker']
        satker_obj = Satker.objects.get(id_satker=get_satker)
        #bulan sekarang
        get_str_date = self.request.session['tgl_report']
        get_month = get_str_date[5:7]
        get_year = get_str_date[0:4]
        lastday = calendar.monthrange(int(get_year), int(get_month))[1]
        
        #bulan sebelum
        parse_date_report = parse_date(get_str_date+"-01")
        get_date_min = str(parse_date_report - relativedelta.relativedelta(months=1))
        get_month_min = get_date_min[5:7]
        get_year_min = get_date_min[0:4]
        lastday_min = calendar.monthrange(int(get_year_min), int(get_month_min))[1]

        # find total value from every category
        kategori_list = Mutasi.objects.values_list('kategori').distinct()
        amount2 = []
        for category in kategori_list:
            category_list = Mutasi.objects.filter(tgl_mutasi__year=get_year, tgl_mutasi__month=get_month, kategori=category[0]).values_list('jumlah_awal', 'nilai_barang', 'masuk', 'keluar')
            total_value = 0
            prev_total_value = 0
            for value_ja, value_nb, value_m, value_k in category_list:
                prev_total_value = prev_total_value + (value_ja * value_nb)
                total_value = total_value + ((value_ja + value_m - value_k) * value_nb)
            amount1 = []
            amount1.append(category[0])
            amount1.append(prev_total_value)
            amount1.append(total_value)
            amount2.append(amount1)

        # find total value from all mutasi
        mutasi_list = self.model.objects.filter(
            tgl_mutasi__year=get_year, tgl_mutasi__month=get_month, id_satker=get_satker).values('jumlah_awal', 'masuk', 'keluar', 'nilai_barang', 'tgl_mutasi')
        jumlah_awal = 0
        masuk = 0
        keluar = 0
        nilai_barang = 0
        total = 0
        for item in mutasi_list:
            jumlah_awal = item['jumlah_awal']
            masuk = item['masuk']
            keluar = item['keluar']
            nilai_barang = item['nilai_barang']
            total = total + ((jumlah_awal + masuk - keluar) * nilai_barang)
        
        #dictionary for date-month
        dict = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April", "05": "Mei",
            "06": "Juni", "07": "Juli", "08": "Agustus", "09": "September", "10": "Oktober",
            "11": "November", "12": "Desember",
        }

        #update kwargs
        self.kwargs.update({
            'satker': satker_obj.nama,
            'get_year': get_year,
            'date_report': str(lastday) + ' ' + dict[get_month].upper() + ' ' + get_year,
            'date_report_min': str(lastday_min) + ' ' + dict[get_month_min].upper() + ' ' + get_year_min,
            'report_type': get_report_type,
            'total_nilai': total,
            'uapkpb': self.request.session['uapkpb'],
            'kode_uapkpb': self.request.session['kode_uapkpb'],
            'kategori_list': amount2,
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class ReportFormView(LoginRequiredMixin, TemplateView):
    template_name = "reports/report_form.html"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if self.kwargs['type'] == "Inventaris":
                self.request.session['report_type'] = self.kwargs['type']
                self.request.session['satker'] = request.POST['satker']
                report_url = 'report:inventaris'
            elif self.kwargs['type'] == "Peminjaman":
                self.request.session['report_type'] = self.kwargs['type']
                self.request.session['satker'] = request.POST['satker']
                self.request.session['tgl_report'] = request.POST['tgl_report']
                report_url = 'report:peminjaman'
            elif self.kwargs['type'] == "Persediaan":
                self.request.session['report_type'] = self.kwargs['type']
                self.request.session['satker'] = request.POST['satker']
                self.request.session['tgl_report'] = request.POST['tgl_report']
                self.request.session['uapkpb'] = request.POST['uapkpb']
                self.request.session['kode_uapkpb'] = request.POST['kode_uapkpb']
                report_url = 'report:persediaan'
            return redirect(report_url)    
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        satker_list = Satker.objects.values_list('id_satker', 'nama').distinct()
        self.kwargs.update({
            'satker_list': satker_list,
            'type_list': ("Inventaris","Peminjaman", "Persediaan")
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class MutasiListView(LoginRequiredMixin, ListView):
    model = Mutasi
    template_name = "report/mutasi_list.html"
    context_object_name = 'mutasi_list'
    ordering = ['-tgl_mutasi']
