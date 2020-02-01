from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import (
    InvAddView,
    InvManageView,
    InvDeleteView,
    InvDetailView,
    InvUpdateView,
    TempatListView,
    RuangListView,
    SatkerListView,
    InvAddExisting,
)

app_name = "inventory"

urlpatterns = [
     path('manage/', InvManageView.as_view(), name="manage"),
     path('add/', InvAddView.as_view(), name="add"),
     path('add-existing-good/', InvAddExisting.as_view(), name="add_existing_good"),
     path('delete/<pk>', InvDeleteView.as_view(), name="delete"),
     path('update/<pk>', InvUpdateView.as_view(), name="update"),
     path('detail/<slug>', InvDetailView.as_view(), name="detail"),
     
     path('tempat-list/', TempatListView.as_view(), name="tempat_list"),
     path('ruang-list/', RuangListView.as_view(), name="ruang_list"),
     path('satker-list/', SatkerListView.as_view(), name="satker_list"),
]