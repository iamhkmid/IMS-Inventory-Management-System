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
	tgl_pengadaan	= forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:mm:ss.SSS'}), required=True)
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
			'user_updated'
		]
		
		