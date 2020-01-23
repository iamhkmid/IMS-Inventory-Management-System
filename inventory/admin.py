from django.contrib import admin

# Register your models here.
from .models import *

class TempatAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_tempat',
		'updated',
	]

class BarangAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_barang',
        'slug',
		'updated',
	]

admin.site.register(Tempat, TempatAdmin)
admin.site.register(Barang, BarangAdmin)