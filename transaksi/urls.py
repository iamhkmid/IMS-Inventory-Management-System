from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "transaksi"

urlpatterns = [
     path('list/', TransaksiListView.as_view(), name="list"),
     path('form-peminjaman/', FormPeminjamanView.as_view(), name="form_peminjaman"),
     path('form-habis-pakai/', FormHabispakaiView.as_view(), name="form_habispakai"),
     path('detail/<slug>', TransDetail.as_view(), name="detail"),
     path('delete/<pk>', TransDeleteView.as_view(), name="delete"),

     path('update-1/<pk>', PeminjamanUpdateView.as_view(), name="update1"),
     path('update-2/<pk>', PersediaanUpdateView.as_view(), name="update2"),
     path('pengembalian/', PengembalianView.as_view(), name="pengembalian"),
     
]