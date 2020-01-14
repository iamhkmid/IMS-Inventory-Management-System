from django.contrib import admin

# Register your models here.
from .models import (
    Barang,
    Tempat,
    Transaksi,
    Users,
)

class BarangAdmin(admin.ModelAdmin):
    readonly_fields=('updated',)
	#autocomplete_fields = ['user']

admin.site.register(Barang, BarangAdmin)
admin.site.register(Tempat)
admin.site.register(Transaksi)
admin.site.register(Users)