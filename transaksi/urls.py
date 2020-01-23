from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "transaksi"

urlpatterns = [
     path('list/', TransaksiListView.as_view(), name="list"),
     path('form-peminjaman/', FormPeminjamanView.as_view(), name="form_peminjaman"),
     path('form-habis-pakai/', FormHabispakaiView.as_view(), name="form_habispakai"),
     path('detail/<slug>', TransDetail.as_view(), name="detail"),
]