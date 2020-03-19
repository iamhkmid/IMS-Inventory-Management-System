from django.forms import ModelForm, Form
from django import forms
from .models import *
from datetime import datetime
from django.conf import settings
import pytz

class BarangForm(ModelForm):
	SATUAN = (
		('Unit','Unit'),
		('Pcs','Pcs'),
		('Pack','Pack'),
		('Box','Box'),
		('Rim','Rim'),
		('Unite','Unite'),
		('Roll','Roll')
		)
	
	JENIS = (
		('Inventaris', 'Inventaris'),
		('Modal', 'Modal'),
		('Persediaan', 'Persediaan')
    )
	
	id_barang		= forms.CharField(required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'xxxxxxx (Length=7)', 'minlength' :'7', 'maxlength' :'7'}))
	satuan			= forms.ChoiceField(required=True, choices=SATUAN)
	jenis			= forms.TypedChoiceField(choices=JENIS, widget=forms.RadioSelect())
	tgl_pengadaan	= forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
	keterangan		= forms.CharField(widget=forms.Textarea(), required=False)
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Barang
		fields = [
			'id_barang',
			'nama',
			'jenis',
			'jumlah_b',
			'satuan',
			'id_kategori',
			'nilai_barang',
			'tgl_pengadaan',
			'id_tempat',
			'keterangan',
		]
	def clean(self):
		cleaned_data = super().clean()
		jenis = cleaned_data.get("jenis")
		id_barang = cleaned_data.get("id_barang")
		nama = cleaned_data.get("nama")
		jumlah_b = cleaned_data.get("jumlah_b")
		nilai_barang = cleaned_data.get("nilai_barang")
		
		barang_list = Barang.objects.values_list('id_barang','nama')
		for value1, value2 in barang_list:
			if id_barang == value1:
				self.add_error('id_barang', "ID barang sudah ada. (" + value1 + " - " + value2 +")")
			if nama == value2:
				self.add_error('nama', "Nama barang sudah ada. (" + value1 + " - " + value2 +")")

		if nilai_barang is not None:
			if nilai_barang<500:
				self.add_error('nilai_barang', "Nilai barang terlalu kecil.")
		if jumlah_b is not None:
			if jumlah_b<1:
				self.add_error('jumlah_b', "Jumlah minimal 1.")
		if id_barang is not None:
			if len(id_barang) != 7:
				self.add_error('id_barang', "ID harus 7 digit angka.")

class UpdateBarangForm(ModelForm):
	SATUAN = (
		('Unit','Unit'),
		('Pcs','Pcs'),
		('Pack','Pack'),
		('Box','Box'),
		('Rim','Rim'),
		('Unite','Unite'),
		('Roll','Roll')
		)
	
	JENIS = (
		('Inventaris', 'Inventaris'),
		('Modal', 'Modal'),
		('Persediaan', 'Persediaan')
    )
	
	id_barang		= forms.CharField(required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'xxxxxxx (Length=7)', 'minlength' :'7', 'maxlength' :'7'}))
	satuan			= forms.ChoiceField(required=True, choices=SATUAN)
	jenis			= forms.TypedChoiceField(choices=JENIS, widget=forms.RadioSelect())
	tgl_pengadaan	= forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
	keterangan		= forms.CharField(widget=forms.Textarea(), required=False)
	user_updated	= forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Barang
		fields = [
			'id_barang',
			'nama',
			'jenis',
			'jumlah_b',
			'satuan',
			'id_kategori',
			'nilai_barang',
			'tgl_pengadaan',
			'id_tempat',
			'keterangan',
		]
	def clean(self):
		cleaned_data = super().clean()
		id_barang = cleaned_data.get("id_barang")
		jumlah_b = cleaned_data.get("jumlah_b")
		nilai_barang = cleaned_data.get("nilai_barang")
		tgl_pengadaan = cleaned_data.get("tgl_pengadaan")
		get_tgl = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
	
		if tgl_pengadaan is not None:
			if get_tgl.year != tgl_pengadaan.year or get_tgl.month != tgl_pengadaan.month:
				self.add_error('tgl_pengambilan', "Transaksi harus pada tahun dan bulan saat ini.")

		if nilai_barang is not None:
			if nilai_barang<500:
				self.add_error('nilai_barang', "Nilai barang terlalu kecil.")
		if jumlah_b is not None:
			if jumlah_b<1:
				self.add_error('jumlah_b', "Jumlah minimal 1.")
		if id_barang is not None:
			if len(id_barang) != 7:
				self.add_error('id_barang', "ID harus 7 digit angka.")



class AddExistingForm(Form):
	id_barang = forms.ModelChoiceField(required=True, queryset=Barang.objects.filter(jenis='Persediaan'))
	jumlah = forms.IntegerField(required=True, widget=forms.NumberInput())
	
	def clean(self):
		cleaned_data = super().clean()
		jumlah = cleaned_data.get("jumlah")
		if jumlah is not None:
			if jumlah<1:
				self.add_error('jumlah', "Jumlah minimal 1.")


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

	def clean(self):
		cleaned_data = super().clean()
		jumlah_b = cleaned_data.get("jumlah_b")
		jumlah_rr = cleaned_data.get("jumlah_rr")
		jumlah_rb = cleaned_data.get("jumlah_rb")
		jumlah_hl = cleaned_data.get("jumlah_hl")
		
		if jumlah_b is not None and jumlah_rr is not None:
			total1 = self.instance.jumlah_b + self.instance.jumlah_rr + self.instance.jumlah_rb + self.instance.jumlah_hl
			total2 = jumlah_b + jumlah_rr + jumlah_rb +jumlah_hl
			if total1 != total2:
				self.add_error('jumlah_b', "Error")
				self.add_error('jumlah_rr', "Error")
				self.add_error('jumlah_rb', "Error")
				self.add_error('jumlah_hl', "Error")
				raise forms.ValidationError('Tidak Sesuai dengan total seluruh.')

		
class KategoriForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Kategori
		fields = [
			'nama'
		]

	def clean(self):
		cleaned_data = super().clean()
		nama = cleaned_data.get("nama")
		
		kategori_list = Kategori.objects.values_list('nama', flat=True)
		for value in kategori_list:
			if nama == value:
				self.add_error('nama', "Nama kategori sudah ada.")

class UpdateKategoriForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Kategori
		fields = [
			'nama'
		]