from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import (
    InventoryList,
    TambahBarang,
)

app_name = "inventory"

urlpatterns = [
     path('manage/', InventoryList.as_view(), name="manage"),
     path('add/', TambahBarang.as_view(), name="add"),
]