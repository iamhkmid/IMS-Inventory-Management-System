from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
from barcode import generate
import os
from datetime import datetime
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


def auto_id_kategori():
    nm_id = 'cat'
    return auto_id(nm_id)


def auto_id(nm):
    num_id = '001'
    width = 3

    if nm == 'loc':
        i_model = Tempat.objects.all().order_by('id_tempat')
    elif nm == 'ruang':
        i_model = Ruang.objects.all().order_by('id_ruang')
    elif nm == 'satker':
        i_model = Satker.objects.all().order_by('id_satker')
    elif nm == 'cat':
        i_model = Kategori.objects.all().order_by('id_kategori')

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
            elif nm == 'cat':
                id_int = item.id_kategori[3:6]

            if id_int != num_id:
                formated = nm + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = nm + str_num_id
                num_id = str_num_id
    return formated


'''def auto_id_barang():
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
    return formated'''
'''def auto_barcode(id_b):
    EAN = barcode.get_barcode_class('ean8')
    ean = EAN(id_b, writer=ImageWriter())
    fullname = ean.save(os.path.join('static/media/barcodes/' + id_b))
    loc = "media/barcodes/" + id_b + ".png"
    return loc'''


class Kategori(models.Model):
    id_kategori = models.CharField(
        max_length=12, default=auto_id_kategori, primary_key=True, editable=False)
    nama = models.CharField(max_length=35)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_kategori)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:kategori_list')

    def __str__(self):
        return self.nama

class Satker(models.Model):
    id_satker = models.CharField(
        max_length=12, default=auto_id_satker, primary_key=True, editable=False)
    nama = models.CharField(max_length=35)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_satker)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:satker_detail', kwargs=url_slug)

    def __str__(self):
        return self.nama


class Ruang(models.Model):
    id_ruang = models.CharField(
        max_length=12, default=auto_id_ruang, primary_key=True, editable=False)
    id_satker = models.ForeignKey(Satker, on_delete=models.CASCADE)
    nama = models.CharField(max_length=35)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_ruang)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:ruang_detail', kwargs=url_slug)

    def __str__(self):
        return "{} | {}".format(self.id_satker.nama, self.nama)


class Tempat(models.Model):
    id_tempat = models.CharField(
        max_length=12, default=auto_id_tempat, primary_key=True, editable=False)
    id_ruang = models.ForeignKey(Ruang, on_delete=models.CASCADE)
    nama = models.CharField(max_length=35)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_tempat)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:tempat_detail', kwargs=url_slug)

    def __str__(self):
        return "{}  |  {}  |  {}".format(self.id_ruang.id_satker.nama, self.id_ruang.nama, self.nama)


class Barang(models.Model):
    id_barang = models.CharField(max_length=8, primary_key=True)
    nama = models.CharField(max_length=35)
    jenis = models.CharField(max_length=20)
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    jumlah_b = models.PositiveIntegerField(null=True, blank=True)
    jumlah_rr = models.PositiveIntegerField(null=True, blank=True)
    jumlah_rb = models.PositiveIntegerField(null=True, blank=True)
    jumlah_hl = models.PositiveIntegerField(null=True, blank=True)
    satuan = models.CharField(max_length=20)
    nilai_barang = models.DecimalField(max_digits=20, decimal_places=0)
    tgl_pengadaan = models.DateTimeField()
    id_tempat = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    keterangan = models.TextField(blank=True)
    in_transaction = models.BooleanField(default=False)
    barcode = models.CharField(max_length=40, null=True, blank=True)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    @property
    def is_past_due(self):
        date_check = self.tgl_pengadaan.month != datetime.now(
        ).month or self.tgl_pengadaan.year != datetime.now().year
        return date_check

    def save(self):
        self.slug = slugify(self.id_barang)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:detail', kwargs=url_slug)

    def __str__(self):
        return "{} - {}".format(self.id_barang, self.nama)
