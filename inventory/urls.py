from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "inventory"

urlpatterns = [
     path('manage/', InvManageView.as_view(), name="manage"),
     path('add/', InvAddView.as_view(), name="add"),
     path('delete/<pk>', InvDeleteView.as_view(), name="delete"),
     path('update/<pk>', InvUpdateView.as_view(), name="update"),
     path('detail/<slug>', InvDetailView.as_view(), name="detail"),
     path('add-existing-good/', InvAddExisting.as_view(), name="add_existing_good"),
     path('condition-update/<pk>', InvConditionUpdateView.as_view(), name="condition_update"),
     path('barcode-print/<pk>', BarcodePrintView.as_view(), name="barcode_print"),
     
     path('tempat-list/', TempatListView.as_view(), name="tempat_list"),
     path('tempat-add/', TempatAddView.as_view(), name="tempat_add"),
     path('tempat-detail/<slug>', TempatDetailView.as_view(), name="tempat_detail"),
     path('ruatempatng-update/<pk>', TempatUpdateView.as_view(), name="tempat_update"),
     path('tempat-del/<pk>', TempatDeleteView.as_view(), name="tempat_del"),
     
     path('ruang-list/', RuangListView.as_view(), name="ruang_list"),
     path('ruang-add/', RuangAddView.as_view(), name="ruang_add"),
     path('ruang-detail/<slug>', RuangDetailView.as_view(), name="ruang_detail"),
     path('ruang-update/<pk>', RuangUpdateView.as_view(), name="ruang_update"),
     path('ruang-del/<pk>', RuangDeleteView.as_view(), name="ruang_del"),

     path('satker-list/', SatkerListView.as_view(), name="satker_list"),
     path('satker-add/', SatkerAddView.as_view(), name="satker_add"),
     path('satker-detail/<slug>', SatkerDetailView.as_view(), name="satker_detail"),
     path('satker-update/<pk>', SatkerUpdateView.as_view(), name="satker_update"),
     path('satker-del/<pk>', SatkerDeleteView.as_view(), name="satker_del"),


     path('kategori-list/', KategoriListView.as_view(), name="kategori_list"),
     path('kategori-add/', KategoriAddView.as_view(), name="kategori_add"),
     path('kategori-update/<pk>', KategoriUpdateView.as_view(), name="kategori_update"),
     path('kategori-del/<pk>', KategoriDeleteView.as_view(), name="kategori_del"),
]
