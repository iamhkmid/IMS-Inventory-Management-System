from django.contrib import admin

# Register your models here.
from .models import *


class TransaksiAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_transaksi',
		'updated',
	]

class UsersAdmin(admin.ModelAdmin):
    readonly_fields=[
		'id_user',
		'updated',
	]

admin.site.register(Users, UsersAdmin)
admin.site.register(Transaksi, TransaksiAdmin)