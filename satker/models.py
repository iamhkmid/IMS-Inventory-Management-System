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

def auto_id(nm):
    num_id = '001'
    width = 3

    if nm == 'loc':
        obj = Tempat.objects.all().order_by('id_tempat')
    elif nm == 'ruang':
        obj = Ruang.objects.all().order_by('id_ruang')
    elif nm == 'satker':
        obj = Satker.objects.all().order_by('id_satker')

    if not obj.last():
        formated = nm + num_id
    else:
        for item in obj:
            if nm == 'loc':
                id_int = item.id_tempat[3:6]
            elif nm == 'ruang':
                id_int = item.id_ruang[5:8]
            elif nm == 'satker':
                id_int = item.id_satker[6:9]

            if id_int != num_id:
                formated = nm + num_id
            else:
                num_id = str(int(num_id)+1)
                str_num_id = str((width - len(num_id)) * "0") + num_id
                formated = nm + str_num_id
                num_id = str_num_id
    return formated


class Satker(models.Model):
    id_satker = models.CharField(
        max_length=12, default=auto_id_satker, primary_key=True, editable=False)
    nama = models.CharField(max_length=35)
    is_used = models.BooleanField(default=False)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_satker)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:satker_detail', kwargs=self.id_satker)

    def __str__(self):
        return self.nama


class Ruang(models.Model):
    id_ruang = models.CharField(
        max_length=12, default=auto_id_ruang, primary_key=True, editable=False)
    id_satker = models.ForeignKey(Satker, on_delete=models.CASCADE)
    nama = models.CharField(max_length=35)
    is_used = models.BooleanField(default=False)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_ruang)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:ruang_detail', kwargs=self.id_ruang)

    def __str__(self):
        return "{} | {}".format(self.id_satker.nama, self.nama)


class Tempat(models.Model):
    id_tempat = models.CharField(
        max_length=12, default=auto_id_tempat, primary_key=True, editable=False)
    id_ruang = models.ForeignKey(Ruang, on_delete=models.CASCADE)
    nama = models.CharField(max_length=35)
    is_used = models.BooleanField(default=False)
    user_updated = models.CharField(max_length=35, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def save(self):
        self.slug = slugify(self.id_tempat)
        super().save()

    def get_absolute_url(self):
        url_slug = {'slug': self.slug}
        return reverse('inventory:tempat_detail', kwargs=self.id_tempat)

    def __str__(self):
        return "{}  |  {}  |  {}".format(self.id_ruang.id_satker.nama, self.id_ruang.nama, self.nama)