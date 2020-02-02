from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


def auto_id_tempat():
    nm_id = 'loc'
    return auto_id(nm_id)


def auto_id_ruang():
    nm_id = 'ruang'
    return auto_id(nm_id)


def auto_id_satker():
    nm_id = 'satker'
    return auto_id(nm_id)


def auto_id_transaksi():
    tr_date = str(timezone.now().strftime('%Y%m%d-'))
    return auto_id(tr_date)


def auto_id(nm):
    num_id = '001'
    width = 3

    if nm == 'loc':
        i_model = Tempat.objects.all().order_by('id_tempat')
    elif nm == 'ruang':
        i_model = Ruang.objects.all().order_by('id_ruang')
    elif nm == 'satker':
        i_model = Satker.objects.all().order_by('id_satker')
    elif nm[8:9] == '-':
        i_model = Transaksi.objects.all().order_by('id_transaksi')

    if not i_model.last():
        formated = nm + num_id
    else:
        for item in i_model:
            if nm == 'loc':
                id_int = item.id_tempat[3:6]
            elif nm == 'ruang':
                id_int = item.id_ruang[5:8]
            elif nm == 'satker':
                id_int = item.id_satker[5:8]
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


def auto_id_barang():
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


class Satker(models.Model):
    id_satker       = models.CharField(
        max_length=12, default=auto_id_satker, primary_key=True, editable=False)
    nama            = models.CharField(max_length=35)
    user_updated    = models.CharField(max_length=35, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.nama)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:satker_detail', kwargs=url_slug)

    def __str__(self):
        return self.nama


class Ruang(models.Model):
    id_ruang        = models.CharField(
        max_length=12, default=auto_id_ruang, primary_key=True, editable=False)
    id_satker       = models.ForeignKey(Satker, on_delete=models.CASCADE)
    nama            = models.CharField(max_length=35)
    user_updated    = models.CharField(max_length=35, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.nama)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:ruang_detail', kwargs=url_slug)

    def __str__(self):
        return "{} | {}".format(self.id_satker.nama, self.nama)


class Tempat(models.Model):
    id_tempat       = models.CharField(
        max_length=12, default=auto_id_tempat, primary_key=True, editable=False)
    id_ruang        = models.ForeignKey(Ruang, on_delete=models.CASCADE)
    nama            = models.CharField(max_length=35)
    user_updated    = models.CharField(max_length=35, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.nama)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:tempat_detail', kwargs=url_slug)

    def __str__(self):
        return "{}  |  {}  |  {}".format(self.id_ruang.id_satker.nama, self.id_ruang.nama, self.nama)


class Barang(models.Model):
    id_barang   = models.CharField(
        max_length=8, default=auto_id_barang, primary_key=True, editable=False)
    nama            = models.CharField(max_length=35)
    jenis           = models.CharField(max_length=20)
    jumlah          = models.IntegerField()
    satuan          = models.CharField(max_length=20)
    nilai_barang    = models.DecimalField(max_digits=20, decimal_places=0)
    tgl_pengadaan   = models.DateTimeField()
    id_tempat       = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    keterangan      = models.TextField(blank=True)
    user_updated    = models.CharField(max_length=35, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    slug            = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_barang)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:detail', kwargs=url_slug)

    def __str__(self):
        return "{} - {}".format(self.id_barang, self.nama)
