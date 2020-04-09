from django.forms import ModelForm, Form
from django import forms
from .models import *
from datetime import datetime
from django.conf import settings
import pytz

class AddExistingForm(Form):
	id_barang = forms.ModelChoiceField(required=True, queryset=Barang.objects.filter(jenis='Persediaan'))
	jumlah = forms.IntegerField(required=True, widget=forms.NumberInput())
	
	def clean(self):
		cleaned_data = super().clean()
		jumlah = cleaned_data.get("jumlah")
		if jumlah is not None:
			if jumlah<1:
				self.add_error('jumlah', "Jumlah minimal 1.")