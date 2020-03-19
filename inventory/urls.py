from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "inventory"

urlpatterns = [
     path('list/barang/', InvManageView.as_view(), name="barang_list"),
     path('add/barang/', InvAddView.as_view(), name="barang_add"),
     path('delete/barang/<pk>', InvDeleteView.as_view(), name="barang_delete"),
     path('update/barang/<pk>', InvUpdateView.as_view(), name="barang_update"),
     path('detail/barang/<pk>', InvDetailView.as_view(), name="barang_detail"),
     path('add-existing/barang/', InvAddExisting.as_view(), name="barang_add_existing"),
     path('condition/barang/<pk>', InvConditionUpdateView.as_view(), name="barang_condition"),
     path('barcode-print/barang/<pk>', BarcodePrintView.as_view(), name="barcode_print"),

     path('list/kategori/', KategoriListView.as_view(), name="kategori_list"),
     path('add/kategori/', KategoriAddView.as_view(), name="kategori_add"),
     path('update/kategori/<pk>', KategoriUpdateView.as_view(), name="kategori_update"),
     path('delete/kategori/<pk>', KategoriDeleteView.as_view(), name="kategori_delele"),
]
