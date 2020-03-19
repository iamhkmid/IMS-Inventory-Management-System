from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "satker"

urlpatterns = [

     path('list/', SatkerListView.as_view(), name="list"),
     path('add/', SatkerAddView.as_view(), name="add"),
     path('detail/<pk>', SatkerDetailView.as_view(), name="detail"),
     path('update/<pk>', SatkerUpdateView.as_view(), name="update"),
     path('delete/<pk>', SatkerDeleteView.as_view(), name="delete"),

     path('list/ruang/', RuangListView.as_view(), name="ruang_list"),
     path('add/ruang/', RuangAddView.as_view(), name="ruang_add"),
     path('detail/ruang/<pk>', RuangDetailView.as_view(), name="ruang_detail"),
     path('update/ruang/<pk>', RuangUpdateView.as_view(), name="ruang_update"),
     path('delete/ruang/<pk>', RuangDeleteView.as_view(), name="ruang_delete"),

     path('list/tempat/', TempatListView.as_view(), name="tempat_list"),
     path('add/tempat/', TempatAddView.as_view(), name="tempat_add"),
     path('detail/tempat/<pk>', TempatDetailView.as_view(), name="tempat_detail"),
     path('update/tempat/<pk>', TempatUpdateView.as_view(), name="tempat_update"),
     path('delete/tempat/<pk>', TempatDeleteView.as_view(), name="tempat_delete"),
     
]
