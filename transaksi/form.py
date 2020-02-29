from django.forms import ModelForm
from django import forms
from .models import *
from inventory.models import Barang


class PeminjamanForm(ModelForm):
    id_barang = forms.ModelChoiceField(Barang.objects.filter(jenis='Inventaris'))
    transaksi = forms.CharField(
        widget=forms.HiddenInput(), initial="Peminjaman")
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS', 'data-target':'#datepicker4'}), required=True)
    tgl_kembali = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS', 'data-target':'#datepicker5'}), required=False)
    keterangan = forms.CharField(widget=forms.Textarea(), required=False)
    user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Transaksi
        fields = [
            'id_barang',
            'transaksi',
            'jumlah',
            'tgl_pengambilan',
            'tgl_kembali',
            'pengguna',
            'keterangan',
            'user_updated'
        ]


class HabispakaiForm(ModelForm):
    id_barang = forms.ModelChoiceField(Barang.objects.filter(jenis='Persediaan'))
    transaksi = forms.CharField(
        widget=forms.HiddenInput(), initial="Persediaan")
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS', 'data-target':'#datepicker4'}), required=True)
    keterangan = forms.CharField(widget=forms.Textarea(), required=False)
    user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Transaksi
        fields = [
            'id_barang',
            'transaksi',
            'jumlah',
            'tgl_pengambilan',
            'pengguna',
            'keterangan',
            'user_updated'
        ]
