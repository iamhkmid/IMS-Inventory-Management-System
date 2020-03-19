from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "reports"

urlpatterns = [
     path('form/<type>', ReportFormView.as_view(), name='ReportForm'),
     path('inventaris/', ReportsInventarisView.as_view(), name="inventaris"),
     path('peminjaman/', ReportsPeminjamanView.as_view(), name="peminjaman"),
     path('persediaan/', ReportsPersediaanView.as_view(), name="persediaan"),
     path('list/mutasi/', MutasiListView.as_view(), name="mutasi"),
]