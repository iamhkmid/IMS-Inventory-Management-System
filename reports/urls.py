from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "reports"

urlpatterns = [
     path('form/inventaris/', FormInventarisView.as_view(), name='form_inventaris'),
     path('form/modal/', FormModalView.as_view(), name='form_modal'),
     path('form/inventaris&modal/', FormInventarisModalView.as_view(), name='form_inventaris_modal'),
     path('form/peminjaman/', FormPeminjamanView.as_view(), name='form_peminjaman'),
     path('form/persediaan/', FormPersediaanView.as_view(), name='form_persediaan'),

     path('inventaris/', ReportsInventarisView.as_view(), name="inventaris"),
     path('modal/', ReportsModalView.as_view(), name="modal"),
     path('inventaris&modal/', ReportsInventarisModalView.as_view(), name="inventaris_modal"),
     path('peminjaman/', ReportsPeminjamanView.as_view(), name="peminjaman"),
     path('persediaan/', ReportsPersediaanView.as_view(), name="persediaan"),
     
     path('list/mutasi/', MutasiListView.as_view(), name="mutasi"),
]