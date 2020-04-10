from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from transaksi.models import Transaksi
from inventory.models import Satker, Kategori
from .models import Mutasi
from inventory.models import Barang
import calendar
from dateutil import relativedelta
from django.utils.dateparse import parse_datetime, parse_date
from django.conf import settings
import pytz
from datetime import datetime
from .form import *


class FormInventarisView(LoginRequiredMixin, FormView):
    template_name = "reports/form_inventaris.html"
    form_class = FormInvetarisModal
    success_url = reverse_lazy('report:inventaris')

    def form_valid(self, form):
        self.form = form
        satker_obj = form.cleaned_data['id_satker']
        self.request.session['satker'] = satker_obj.id_satker
        return HttpResponseRedirect(self.get_success_url())

class FormModalView(LoginRequiredMixin, FormView):
    template_name = "reports/form_modal.html"
    form_class = FormInvetarisModal
    success_url = reverse_lazy('report:modal')

    def form_valid(self, form):
        self.form = form
        satker_obj = form.cleaned_data['id_satker']
        self.request.session['satker'] = satker_obj.id_satker
        return HttpResponseRedirect(self.get_success_url())

class FormInventarisModalView(LoginRequiredMixin, FormView):
    template_name = "reports/form_invantaris_modal.html"
    form_class = FormInvetarisModal
    success_url = reverse_lazy('report:inventaris_modal')

    def form_valid(self, form):
        self.form = form
        satker_obj = form.cleaned_data['id_satker']
        self.request.session['satker'] = satker_obj.id_satker
        return HttpResponseRedirect(self.get_success_url())


class FormPeminjamanView(LoginRequiredMixin, FormView):
    template_name = "reports/form_peminjaman.html"
    form_class = FormPeminjaman
    success_url = reverse_lazy('report:peminjaman')

    def form_valid(self, form):
        self.form = form
        satker_obj = form.cleaned_data['id_satker']
        self.request.session['satker'] = satker_obj.id_satker
        self.request.session['tgl_report'] = str(
            form.cleaned_data['tgl_report'])
        return HttpResponseRedirect(self.get_success_url())


class FormPersediaanView(LoginRequiredMixin, FormView):
    template_name = "reports/form_persediaan.html"
    form_class = FormPersediaan
    success_url = reverse_lazy('report:persediaan')

    def form_valid(self, form):
        self.form = form
        print(str(form.cleaned_data['tgl_report']))
        satker_obj = form.cleaned_data['id_satker']
        self.request.session['satker'] = satker_obj.id_satker
        self.request.session['tgl_report'] = str(
            form.cleaned_data['tgl_report'])
        self.request.session['uapkpb'] = form.cleaned_data['uapkpb']
        self.request.session['kode_uapkpb'] = form.cleaned_data['kode_uapkpb']
        return HttpResponseRedirect(self.get_success_url())


class ReportsInventarisView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "reports/report_inventaris_modal.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

    def get_queryset(self):
        self.queryset = self.model.objects.filter(jenis="Inventaris")
        return super().get_queryset()

    def get_context_data(self, **kwargs):
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

        ruang_list = Barang.objects.filter(jenis="Inventaris").values_list(
            "id_tempat__id_ruang", "id_tempat__id_ruang__nama").distinct()

        satker_list = Satker.objects.values_list(
            'id_satker', 'nama').distinct()
        self.kwargs.update({
            'get_satker': satker_obj.nama.upper(),
            'date_report': str(get_day) + ' ' + dict[get_month].upper() + ' ' + str(get_year),
            'ruang_list': ruang_list,
            'satker_list': satker_list,
            'url_back' : 'reports:form_inventaris',
            'report_name' : 'INVENTARISASI',
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class ReportsModalView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "reports/report_inventaris_modal.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

    def get_queryset(self):
        self.queryset = self.model.objects.filter(jenis="Modal")
        return super().get_queryset()

    def get_context_data(self, **kwargs):
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

        ruang_list = Barang.objects.filter(jenis="Modal").values_list(
            "id_tempat__id_ruang", "id_tempat__id_ruang__nama").distinct()

        satker_list = Satker.objects.values_list(
            'id_satker', 'nama').distinct()
        self.kwargs.update({
            'get_satker': satker_obj.nama.upper(),
            'date_report': str(get_day) + ' ' + dict[get_month].upper() + ' ' + str(get_year),
            'ruang_list': ruang_list,
            'satker_list': satker_list,
            'url_back' : 'reports:form_modal',
            'report_name' : 'BARANG MODAL',
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context

class ReportsInventarisModalView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = "reports/report_inventaris_modal.html"
    context_object_name = 'barang_list'
    ordering = ['id_barang']

    def get_queryset(self):
        self.queryset = self.model.objects.exclude(jenis="Persediaan")
        return super().get_queryset()

    def get_context_data(self, **kwargs):
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

        ruang_list = Barang.objects.exclude(jenis="Persediaan").values_list(
            "id_tempat__id_ruang", "id_tempat__id_ruang__nama").distinct()
        print(ruang_list)

        satker_list = Satker.objects.values_list(
            'id_satker', 'nama').distinct()
        self.kwargs.update({
            'get_satker': satker_obj.nama.upper(),
            'date_report': str(get_day) + ' ' + dict[get_month].upper() + ' ' + str(get_year),
            'ruang_list': ruang_list,
            'satker_list': satker_list,
            'url_back' : 'reports:form_inventaris_modal',
            'report_name' : 'INVENTARISASI & MODAL',
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
        self.queryset = self.model.objects.filter(tgl_pengambilan__year=get_year, tgl_pengambilan__month=get_month,
                                                  transaksi="Peminjaman", id_barang__id_tempat__id_ruang__id_satker=get_satker)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
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
        get_satker = self.request.session['satker']
        satker_obj = Satker.objects.get(id_satker=get_satker)
        # bulan sekarang
        get_str_date = self.request.session['tgl_report']
        get_month = get_str_date[5:7]
        get_year = get_str_date[0:4]
        lastday = calendar.monthrange(int(get_year), int(get_month))[1]

        # bulan sebelum
        parse_date_report = parse_date(get_str_date)
        get_date_min = str(parse_date_report -
                           relativedelta.relativedelta(months=1))
        get_month_min = get_date_min[5:7]
        get_year_min = get_date_min[0:4]
        lastday_min = calendar.monthrange(
            int(get_year_min), int(get_month_min))[1]

        # find total value from every category
        category_list = Mutasi.objects.values_list('kategori', flat=True).filter(
            tgl_mutasi__year=get_year, tgl_mutasi__month=get_month).distinct()
        amount2 = []
        for category in category_list:
            mutasi_list = Mutasi.objects.filter(tgl_mutasi__year=get_year, tgl_mutasi__month=get_month, kategori=category).values_list(
                'jumlah_awal', 'nilai_barang', 'masuk', 'keluar')
            category_obj = Kategori.objects.get(id_kategori=category)
            total_value = 0
            prev_total_value = 0
            for value_ja, value_nb, value_m, value_k in mutasi_list:
                prev_total_value = prev_total_value + (value_ja * value_nb)
                total_value = total_value + \
                    ((value_ja + value_m - value_k) * value_nb)
            amount1 = []
            amount1.append(category)
            amount1.append(category_obj.nama)
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

        # dictionary for date-month
        dict = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April", "05": "Mei",
            "06": "Juni", "07": "Juli", "08": "Agustus", "09": "September", "10": "Oktober",
            "11": "November", "12": "Desember",
        }

        # update kwargs
        self.kwargs.update({
            'satker': satker_obj.nama,
            'get_year': get_year,
            'date_report': str(lastday) + ' ' + dict[get_month].upper() + ' ' + get_year,
            'date_report_min': str(lastday_min) + ' ' + dict[get_month_min].upper() + ' ' + get_year_min,
            'total_nilai': total,
            'uapkpb': self.request.session['uapkpb'],
            'kode_uapkpb': self.request.session['kode_uapkpb'],
            'kategori_list': amount2,
        })
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


class MutasiListView(LoginRequiredMixin, ListView):
    model = Mutasi
    template_name = "report/mutasi_list.html"
    context_object_name = 'mutasi_list'
    ordering = ['-tgl_mutasi']
