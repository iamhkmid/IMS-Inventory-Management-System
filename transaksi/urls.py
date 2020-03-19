from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "transaksi"

urlpatterns = [
     path('list/', TransaksiListView.as_view(), name="transaksi_list"),
     path('form/peminjaman/', FormPeminjamanView.as_view(), name="transaksi_form1"),
     path('form/pengembalian/', PengembalianView.as_view(), name="transaksi_form2"),
     path('form/habispakai/', FormHabispakaiView.as_view(), name="transaksi_form3"),
     path('detail/<pk>', TransaksiDetail.as_view(), name="transaksi_detail"),
     path('delete/<pk>', TransDeleteView.as_view(), name="transaksi_delete"),
     path('update/peminjaman/<pk>', PeminjamanUpdateView.as_view(), name="transaksi_update1"),
     path('update/habispakai/<pk>', HabisPakaiUpdateView.as_view(), name="transaksi_update2"),
     
]