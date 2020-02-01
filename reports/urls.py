from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "reports"

urlpatterns = [
     path('choose/', ChooseReportsView.as_view(), name='choose'),
     path('report-peminjaman/', ReportsPeminjamanView.as_view(), name="peminjaman"),
     path('report-persediaan/', ReportsPersediaanView.as_view(), name="persediaan"),
     path('mutasi-list/', MutasiListView.as_view(), name="mutasi"),
     
]