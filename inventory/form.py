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
		('Unit','Unit'),
		('Pcs','Pcs'),
		('Pack','Pack'),
		('Box','Box'),
		('Rim','Rim'),
		('Unite','Unite'),
		('Roll','Roll')
		)
	
	id_barang		= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'xxxxxxx (Length=7)', 'minlength' :'7', 'maxlength' :'7'}))
	jenis			= forms.TypedChoiceField(required=True, choices=JENIS, widget=forms.RadioSelect)
	satuan			= forms.TypedChoiceField(required=True, choices=SATUAN)
	tgl_pengadaan	= forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS', 'data-target':'#datepicker4'}), required=True)
	keterangan		= forms.CharField(widget=forms.Textarea(), required=False)
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Barang
		fields = [
			'id_barang',
			'nama',
			'jenis',
			'jumlah',
			'satuan',
			'id_kategori',
			'nilai_barang',
			'tgl_pengadaan',
			'id_tempat',
			'keterangan',
		]


class ConditionUpdateForm(ModelForm):
	jumlah_b = forms.IntegerField(widget=forms.NumberInput(attrs={'autofocus': 'autofocus', 'min': 0,}),required=True)
	jumlah_rr = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,}),required=True)
	jumlah_rb = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,}),required=True)
	jumlah_hl = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,}),required=True)
	class Meta:
		model = Barang
		fields = [
			'jumlah_b',
			'jumlah_rr',
			'jumlah_rb',
			'jumlah_hl',
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
		
class KategoriForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Kategori
		fields = [
			'nama'
		]