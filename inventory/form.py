from django.forms import ModelForm
from django import forms
from .models import *

class BarangForm(ModelForm):

	class Meta:
		model = Barang
		fields = [
			'nama',
			'jenis',
			'jumlah',
			'satuan',
			'nilai_barang',
			'satker',
			'tgl_pengadaan',
			'tempat',
			'keterangan',
		]
		