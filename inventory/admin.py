from django.contrib import admin

# Register your models here.
from .models import *

class SatkerAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_satker',
		'updated',
	]

class RuangAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_ruang',
		'updated',
	]

class TempatAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_tempat',
		'updated',
	]

class BarangAdmin(admin.ModelAdmin):
    readonly_fields=[
        'slug',
		'updated',
	]

class KategoriAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_kategori',
		'updated',
	]

admin.site.register(Satker, SatkerAdmin)
admin.site.register(Ruang, RuangAdmin)
admin.site.register(Tempat, TempatAdmin)
admin.site.register(Barang, BarangAdmin)
admin.site.register(Kategori, KategoriAdmin)