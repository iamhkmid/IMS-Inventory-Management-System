from django.forms import ModelForm
from .models import Barang


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
			'keterangan',
		]