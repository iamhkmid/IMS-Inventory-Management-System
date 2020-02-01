from django.forms import ModelForm
from django import forms
from .models import *


class PeminjamanForm(ModelForm):
    transaksi = forms.CharField(
        widget=forms.HiddenInput(), initial="Peminjaman")
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
    tgl_kembali = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=False)
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
    transaksi = forms.CharField(
        widget=forms.HiddenInput(), initial="Persediaan")
    tgl_pengambilan = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
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
