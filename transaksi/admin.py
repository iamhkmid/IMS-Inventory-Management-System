from django.contrib import admin

# Register your models here.
from .models import *


class TransaksiAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_transaksi',
		'updated',
        'slug',
	]

admin.site.register(Transaksi, TransaksiAdmin)