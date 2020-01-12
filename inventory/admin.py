from django.contrib import admin

# Register your models here.
from .models import Barang

class BarangAdmin(admin.ModelAdmin):
    readonly_fields=('updated',)
	#autocomplete_fields = ['user']

admin.site.register(Barang, BarangAdmin)