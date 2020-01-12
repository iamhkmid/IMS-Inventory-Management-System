from django.db import models

# Create your models here.
def incerement_id_barang():
    last_id_barang = Barang.objects.all().order_by('id_barang').last()
    if not last_id_barang:
        return '0000001'
    width = 7
    id_barang_int = int(last_id_barang.id_barang)
    new_id_barang = str(id_barang_int + 1)
    print(type(new_id_barang))
    formated = str((width - len(new_id_barang)) * "0") + new_id_barang
    return formated

class Barang(models.Model):
    JENIS = (
        ('Inventaris', 'Inventaris'),
        ('Modal', 'Modal'),
        ('Persediaan', 'Persediaan'),
    )
    SATUAN = (
        ('Persediaan', 'Pak'),
        ('Buah', 'Buah'),
        ('Kotak', 'Kotak'),
    )
    id_barang = models.CharField(max_length=8, default = incerement_id_barang, primary_key=True, editable = False)
    nama = models.CharField(max_length=35)
    jenis = models.CharField(max_length=35, choices = JENIS)
    jumlah = models.PositiveIntegerField()
    satuan = models.CharField(max_length=10, choices = SATUAN)
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
