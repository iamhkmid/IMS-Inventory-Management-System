from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from inventory.models import Barang, Satker
from transaksi.models import Transaksi


def auto_id():
    nm = str(timezone.now().strftime('%Y%m%d-'))
    num_id = '001'
    width = 3

    i_model = Mutasi.objects.all().order_by('id_mutasi')

    if not i_model.last():
        formated = nm + num_id
    else:
        for item in i_model:
            id_int = item.id_mutasi[9:12]

            if id_int != num_id:
                formated = nm + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = nm + str_num_id
                num_id = str_num_id
    return formated


class Mutasi(models.Model):
    id_mutasi       = models.CharField(
        max_length=13, default=auto_id, primary_key=True, editable=False)
    id_barang       = models.CharField(max_length=10)
    nama_barang     = models.CharField(max_length=30)
    kategori        = models.CharField(max_length=30)
    id_satker       = models.ForeignKey(Satker, on_delete=models.CASCADE)
    tgl_mutasi      = models.DateTimeField()
    #tgl_kembali = models.DateTimeField(null=True, blank=True)
    #pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    nilai_barang    = models.PositiveIntegerField()
    jumlah_awal  = models.PositiveIntegerField()
    masuk           = models.PositiveIntegerField()
    keluar          = models.PositiveIntegerField()
    #keterangan = models.TextField(blank=True)
    user_updated    = models.CharField(max_length=35, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_mutasi)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:detail', kwargs=url_slug)

    def __str__(self):
        return "{} - {}".format(self.id_mutasi, self.nama_barang)
