from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
def auto_increment_id():
    id_b = '0000001'
    width = 7
    if not Barang.objects.all().order_by('id_barang').last():
        formated = id_b
    else:  
        for item in Barang.objects.all().order_by('id_barang'):
            if item.id_barang != id_b:
                formated = id_b
            else:
                id_b = str(int(id_b)+1)
                formated = str((width - len(id_b)) * "0") + id_b
                id_b = formated
    return formated

class Tempat(models.Model):
    id_tempat   = models.CharField(max_length=15, primary_key=True)
    nama        = models.CharField(max_length=35)

    def __str__(self):
        return "{} - {}".format(self.id_tempat, self.nama)

class Users(models.Model):
    id_user     = models.CharField(max_length=15, primary_key=True)
    nama        = models.CharField(max_length=35)


class Barang(models.Model):
    id_barang       = models.CharField(max_length=8, default = auto_increment_id, primary_key=True, editable = False)
    nama            = models.CharField(max_length=35)
    jenis           = models.CharField(max_length=20)
    jumlah          = models.IntegerField()
    satuan          = models.CharField(max_length=20)
    nilai_barang    = models.DecimalField(max_digits=20, decimal_places=0)
    satker          = models.CharField(max_length=35)
    tgl_pengadaan   = models.DateTimeField()
    tempat          = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    keterangan      = models.TextField()
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.nama)
        super().save()
    
    def get_absolute_url(self):
        url_slug = {'slug':self.slug}
        return reverse('inventory:detail', kwargs = url_slug)
    
    def __str__(self):
        return "{} - {}".format(self.id_barang, self.nama)


class Transaksi(models.Model):
    id_transaksi        = models.CharField(max_length=15, primary_key=True)
    id_barang           = models.ForeignKey(Barang, on_delete=models.CASCADE)
    nama                = models.CharField(max_length=35)
    tgl_pengambilan     = models.DateTimeField()
    tgl_kembali         = models.DateTimeField(blank = True)
    peminjam            = models.ForeignKey(Users, on_delete=models.CASCADE)
    jumlah              = models.PositiveIntegerField()
