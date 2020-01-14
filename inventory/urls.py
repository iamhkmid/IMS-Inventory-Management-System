from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import (
    InvAddView,
    InvManageView,
    InvDeleteView,
)

app_name = "inventory"

urlpatterns = [
     path('manage/', InvManageView.as_view(), name="manage"),
     path('add/', InvAddView.as_view(), name="add"),
     path('delete/<pk>', InvDeleteView.as_view(), name="delete"),
]