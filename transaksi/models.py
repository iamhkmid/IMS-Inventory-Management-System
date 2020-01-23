from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from inventory.models import Barang

def auto_id_tempat():
    nm_id = 'loc'
    return auto_id(nm_id)

def auto_id_user():
    nm_id = 'usr'
    return auto_id(nm_id)
    
def auto_id_transaksi():
    tr_date = str(timezone.now().strftime('%Y%m%d-'))
    return auto_id(tr_date)

def auto_id(nm):
    num_id = '001'
    width = 3

    if nm == 'loc':
        i_model = Tempat.objects.all().order_by('id_tempat')
    elif nm == 'usr':
        i_model = Users.objects.all().order_by('id_user')
    elif nm[8:9] == '-':
         i_model = Transaksi.objects.all().order_by('id_transaksi')

    if not i_model.last():
        formated = nm + num_id
    else:  
        for item in i_model:
            if nm == 'loc':
                id_int = item.id_tempat[3:6]
            elif nm == 'usr':
                id_int = item.id_user[3:6]
            elif nm[8:9] == '-':
                id_int = item.id_transaksi[9:12]

            if id_int != num_id:
                formated = nm + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = nm + str_num_id
                num_id = str_num_id
    return formated

class Users(models.Model):
    id_user     = models.CharField(max_length=8, default = auto_id_user, primary_key=True, editable = False)
    nama        = models.CharField(max_length=35)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id_user, self.nama)

class Transaksi(models.Model):
    id_transaksi        = models.CharField(max_length=13, default = auto_id_transaksi, primary_key=True, editable = False)
    id_barang           = models.ForeignKey(Barang, on_delete=models.CASCADE)
    transaksi           = models.CharField(max_length=13)
    tgl_pengambilan     = models.DateTimeField()
    tgl_kembali         = models.DateTimeField(blank = True)
    pengguna            = models.ForeignKey(Users, on_delete=models.CASCADE)
    jumlah              = models.PositiveIntegerField()
    keterangan          = models.TextField()
    updated             = models.DateTimeField(auto_now=True)
    slug                = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_transaksi)
        super().save()
    
    def get_absolute_url(self):
        url_slug = {'slug':self.slug}
        return reverse('transaksi:detail', kwargs = url_slug)

    def __str__(self):
        return "{} - {} - {}".format(self.id_transaksi, self.id_barang.nama, self.peminjam.nama)

