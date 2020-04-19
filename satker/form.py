from django.forms import ModelForm, Form
from django import forms
from .models import *
from datetime import datetime
from django.conf import settings
import pytz

class SatkerForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Satker
		fields = [
			'nama',
		]
	
	def clean(self):
		cleaned_data = super().clean()
		nama = cleaned_data.get("nama")
		
		satker_list = Satker.objects.values_list('nama', flat=True)
		for value in satker_list:
			if nama == value:
				self.add_error('nama', "Nama satker sudah ada.")

class UpdateSatkerForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Satker
		fields = [
			'nama',
		]

class RuangForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Ruang
		fields = [
			'nama',
			'id_satker',
		]
	
	def clean(self):
		cleaned_data = super().clean()
		nama = cleaned_data.get("nama")
		
		ruang_list = Ruang.objects.values_list('nama', flat=True)
		for value in ruang_list:
			if nama == value:
				self.add_error('nama', "Nama ruang sudah ada.")

class UpdateRuangForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Ruang
		fields = [
			'nama',
			'id_satker',
		]

class TempatForm(ModelForm):
	nama			= forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
	class Meta:
		model = Tempat
		fields = [
			'nama',
			'id_ruang',
		]
