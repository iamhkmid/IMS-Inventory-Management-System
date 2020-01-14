from django.db import models

# Create your models here.
def auto_increment_id():
    id_b = '0000001'
    width = 7
    for item in Barang.objects.all().order_by('id_barang'):
        if item.id_barang != id_b:
            formated = id_b
        else:
            id_b = str(int(id_b)+1)
            formated = str((width - len(id_b)) * "0") + id_b
            id_b = formated
    return formated

class Barang(models.Model):
    JENIS = (
        ('Inventaris', 'Inventaris'),
        ('Modal', 'Modal'),
        ('Persediaan', 'Persediaan'),
    )
    SATUAN = (
        ('Pak', 'Pak'),
        ('Buah', 'Buah'),
        ('Kotak', 'Kotak'),
    )
    id_barang = models.CharField(max_length=8, default = auto_increment_id, primary_key=True, editable = False)
    nama = models.CharField(max_length=35)
    jenis = models.CharField(max_length=20, choices = JENIS)
    jumlah = models.PositiveIntegerField()
    satuan = models.CharField(max_length=20, choices = SATUAN)
    nilai_barang = models.DecimalField(max_digits=20, decimal_places=0)
    satker = models.CharField(max_length=35)
    tgl_pengadaan = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    keterangan = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id_barang, self.nama)

class Tempat(models.Model):
    id_tempat = models.CharField(max_length=15, primary_key=True)
    nama = models.CharField(max_length=35)
