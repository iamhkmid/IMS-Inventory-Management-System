from django.forms import ModelForm
from django import forms
from .models import *

class BarangForm(ModelForm):
	JENIS = (
		('Inventaris', 'Inventaris'),
		('Modal', 'Modal'),
		('Persediaan', 'Persediaan')
    )
	SATUAN = (
		('Pak','Pak'),
		('Buah','Buah'),
		('Kotak','Kotak')
	)
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	jenis			= forms.TypedChoiceField(required=True, choices=JENIS, widget=forms.RadioSelect)
	satuan			= forms.TypedChoiceField(required=True, choices=SATUAN, widget=forms.RadioSelect)
	tgl_pengadaan	= forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS', 'data-target':'#datepicker4'}), required=True)
	keterangan		= forms.CharField(widget=forms.Textarea(), required=False)
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Barang
		fields = [
			'nama',
			'jenis',
			'jumlah',
			'satuan',
			'nilai_barang',
			'tgl_pengadaan',
			'id_tempat',
			'keterangan',
		]


class SatkerForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)
	class Meta:
		model = Satker
		fields = [
			'nama',
			'user_updated'
		]

class RuangForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)
	class Meta:
		model = Ruang
		fields = [
			'nama',
			'id_satker',
			'user_updated'
		]

class TempatForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)
	class Meta:
		model = Tempat
		fields = [
			'nama',
			'id_ruang',
			'user_updated'
		]
		
		