from django.contrib import admin

# Register your models here.
from .models import *


class MutasiAdmin(admin.ModelAdmin):
    readonly_fields=[
		'updated'
	]

admin.site.register(Mutasi, MutasiAdmin)