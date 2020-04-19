from django.forms import Form, ModelForm
from django import forms
from satker.models import Satker
from datetime import datetime
from django.conf import settings
import pytz

class FormInvetarisModal(Form):
	id_satker = forms.ModelChoiceField(required=True, queryset=Satker.objects.all())


class FormPeminjaman(Form):
	id_satker = forms.ModelChoiceField(required=True, queryset=Satker.objects.all())
	tgl_report = forms.DateField(input_formats=["%Y-%m"], widget=forms.DateInput(
        attrs={'placeholder': 'YYYY-MM'}), required=True)

class FormPersediaan(Form):
	id_satker = forms.ModelChoiceField(required=True, queryset=Satker.objects.all())
	tgl_report = forms.DateField(input_formats=["%Y-%m"], widget=forms.DateInput(
        attrs={'placeholder': 'YYYY-MM'}), required=True)
	uapkpb = forms.CharField(required=True)
	kode_uapkpb = forms.CharField(required=True)