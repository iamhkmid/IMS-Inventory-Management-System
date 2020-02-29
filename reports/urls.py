from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "reports"

urlpatterns = [
     path('reportForm/<type>', ReportFormView.as_view(), name='ReportForm'),

     path('report-inventaris/', ReportsInventarisView.as_view(), name="inventaris"),
     path('report-peminjaman/', ReportsPeminjamanView.as_view(), name="peminjaman"),
     path('report-persediaan/', ReportsPersediaanView.as_view(), name="persediaan"),
     path('mutasi-list/', MutasiListView.as_view(), name="mutasi"),    
]