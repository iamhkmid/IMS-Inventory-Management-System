from django.forms import ModelForm
from django import forms
from .models import *
from bootstrap_datepicker_plus import DateTimePickerInput

class BarangForm(ModelForm):

	jenis = forms.ChoiceField(choices=Barang.JENIS)
	satuan = forms.ChoiceField(choices=Barang.SATUAN)
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
			'keterangan',
		]
		widgets = {
            'tgl_pengadaan': DateTimePickerInput(),
		}