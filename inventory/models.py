from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
from barcode import generate
import os
from satker.models import *
from datetime import datetime

# Create your models here.

def auto_id_kategori():
    nm = 'cat'
    num_id = '001'
    width = 3
    kategori_obj = Kategori.objects.all().order_by('id_kategori')
    if not kategori_obj.last():
        formated = nm + num_id
    else:
        for item in kategori_obj:
            id_int = item.id_kategori[3:6]

            if id_int != num_id:
                formated = nm + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = nm + str_num_id
                num_id = str_num_id
    return formated


class Kategori(models.Model):
    id_kategori = models.CharField(
        max_length=12, default=auto_id_kategori, primary_key=True, editable=False)
    nama = models.CharField(max_length=35)
    is_used = models.BooleanField(default=False)
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


class Barang(models.Model):
    id_barang = models.CharField(max_length=8, primary_key=True)
    nama = models.CharField(max_length=35)
    jenis = models.CharField(max_length=20)
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    jumlah_b = models.PositiveIntegerField()
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

    @property
    def jumlah(self):
        jumlah = self.jumlah_b + self.jumlah_rr
        return jumlah

    def save(self):
        self.slug = slugify(self.id_barang)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:barang_detail', kwargs={'pk': self.id_barang})

    def __str__(self):
        return "{} - {}".format(self.id_barang, self.nama)
