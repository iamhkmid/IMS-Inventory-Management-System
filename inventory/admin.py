from django.contrib import admin

# Register your models here.
from .models import (
    Barang,
    Tempat,
    Transaksi,
    Users,
)

class BarangAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_barang',
        'slug',
		'updated',
	]

admin.site.register(Barang, BarangAdmin)
admin.site.register(Tempat)
admin.site.register(Transaksi)
admin.site.register(Users)