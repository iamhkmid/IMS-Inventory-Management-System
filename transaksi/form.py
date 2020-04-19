from django.forms import ModelForm, Form
from django import forms
from .models import *
from datetime import datetime
import pytz
from django.conf import settings
from inventory.models import Barang


class PeminjamanForm(ModelForm):
    id_barang = forms.ModelChoiceField(Barang.objects.filter(jenis='Inventaris'))
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
    tgl_kembali = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=False)
    keterangan = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Transaksi
        fields = [
            'id_barang',
            'jumlah',
            'tgl_pengambilan',
            'tgl_kembali',
            'pengguna',
            'keterangan',
        ]

    def clean(self):
        cleaned_data = super().clean()
        barang_obj = cleaned_data.get("id_barang")
        jumlah = cleaned_data.get("jumlah")

        if jumlah is not None:
            if barang_obj is not None:
                tot = barang_obj.jumlah - jumlah
                if  tot < 0:
                    self.add_error('jumlah', "Jumlah barang tidak mencukupi. (Tersedia:" + str(barang_obj.jumlah) +")")

            if jumlah<1:
                self.add_error('jumlah', "Jumlah minimal 1.")


class HabispakaiForm(ModelForm):
    id_barang = forms.ModelChoiceField(Barang.objects.filter(jenis='Persediaan'))
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
    keterangan = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Transaksi
        fields = [
            'id_barang',
            'jumlah',
            'tgl_pengambilan',
            'pengguna',
            'keterangan',
        ]

    def clean(self):
        cleaned_data = super().clean()
        barang_obj = cleaned_data.get("id_barang")
        jumlah = cleaned_data.get("jumlah")
        tgl_pengambilan = cleaned_data.get("tgl_pengambilan")
        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

        if tgl_pengambilan is not None:
            if get_tgl.year != tgl_pengambilan.year or get_tgl.month != tgl_pengambilan.month:
                self.add_error('tgl_pengambilan', "Transaksi harus pada tahun dan bulan saat ini.")

        if jumlah is not None:
            if barang_obj is not None:
                tot = barang_obj.jumlah - jumlah
                if  tot < 0:
                    self.add_error('jumlah', "Jumlah barang tidak mencukupi. (Tersedia:" + str(barang_obj.jumlah) +")")
            if jumlah<1:
                self.add_error('jumlah', "Jumlah minimal 1.")
    
class UpdateHabispakaiForm(ModelForm):
    id_barang = forms.ModelChoiceField(Barang.objects.filter(jenis='Persediaan'))
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
    keterangan = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Transaksi
        fields = [
            'id_barang',
            'jumlah',
            'tgl_pengambilan',
            'pengguna',
            'keterangan',
        ]

    def clean(self):
        cleaned_data = super().clean()
        barang_obj = cleaned_data.get("id_barang")
        transaksi_obj = Transaksi.objects.get(id_transaksi=self.instance.id_transaksi)
        jumlah = cleaned_data.get("jumlah")
        tgl_pengambilan = cleaned_data.get("tgl_pengambilan")
        get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

        if tgl_pengambilan is not None:
            if get_tgl.year != tgl_pengambilan.year or get_tgl.month != tgl_pengambilan.month:
                self.add_error('tgl_pengambilan', "Transaksi harus pada tahun dan bulan saat ini.")

        if jumlah is not None:
            if barang_obj is not None:
                barang_jumlah = barang_obj.jumlah
                tot = barang_jumlah + (transaksi_obj.jumlah - jumlah)
                if  tot < 0:
                    self.add_error('jumlah', "Jumlah barang tidak mencukupi. (Tersedia:" + str(barang_obj.jumlah + transaksi_obj.jumlah) +")")
            if jumlah<1:
                self.add_error('jumlah', "Jumlah minimal 1.")


def transaksiList():
    new_list=[]
    transaksi_list = Transaksi.objects.all().filter(transaksi='Peminjaman').values_list("id_transaksi", flat=True)
    pack2=[None,"--------"]
    new_list.append(pack2)
    for id_trans in transaksi_list:
        transaksi_obj = Transaksi.objects.all().get(id_transaksi=id_trans)
        if transaksi_obj.tgl_kembali is None:
            pack1=[]
            pack1.append(transaksi_obj.id_transaksi)
            pack1.append(transaksi_obj.id_transaksi + " - " + transaksi_obj.pengguna + " : (" + str(transaksi_obj.id_barang) + ")" )
            new_list.append(pack1)	
    return new_list

class PengembalianForm(Form):
    transaksi	= forms.ChoiceField(required=True, choices=transaksiList, widget=forms.Select(attrs={'autofocus': 'autofocus'}))
    tgl_kembali = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        transaksi = cleaned_data.get("transaksi")
        tgl_kembali = cleaned_data.get("tgl_kembali")

        if transaksi is not None and tgl_kembali is not None:
            try:
                transaksi_obj = Transaksi.objects.all().get(id_transaksi=transaksi)
                if tgl_kembali < transaksi_obj.tgl_pengambilan:
                    self.add_error('tgl_kembali', "Tgl kembali tidak boleh kurang dari tgl pengambilan. (" + str(transaksi_obj.tgl_pengambilan) + ")")
            except Exception as err:
                pass
            