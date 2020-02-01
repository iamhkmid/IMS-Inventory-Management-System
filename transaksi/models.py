from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from inventory.models import Barang


def auto_id():
    tr_date = str(timezone.now().strftime('%Y%m%d-'))
    num_id = '001'
    width = 3
    i_model = Transaksi.objects.all().order_by('id_transaksi')

    if not i_model.last():
        formated = tr_date + num_id
    else:
        for item in i_model:
            id_int = item.id_transaksi[9:12]

            if id_int != num_id:
                formated = tr_date + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = tr_date + str_num_id
                num_id = str_num_id
    return formated

class Transaksi(models.Model):
    id_transaksi        = models.CharField(
        max_length=13, default=auto_id, primary_key=True, editable=False)
    id_barang           = models.ForeignKey(Barang, on_delete=models.CASCADE)
    transaksi           = models.CharField(max_length=13)
    tgl_pengambilan     = models.DateTimeField()
    tgl_kembali         = models.DateTimeField(null=True, blank=True)
    pengguna            = models.CharField(max_length=35)
    jumlah              = models.PositiveIntegerField()
    keterangan          = models.TextField(blank=True)
    user_updated        = models.CharField(max_length=35, blank=True)
    updated             = models.DateTimeField(auto_now=True)
    slug                = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_transaksi)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('transaksi:detail', kwargs=url_slug)

    def __str__(self):
        return "{} - {} - {}".format(self.id_transaksi, self.id_barang.nama, self.pengguna)
