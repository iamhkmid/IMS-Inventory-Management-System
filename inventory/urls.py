from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import (
    InvAddView,
    InvManageView,
    InvDeleteView,
    InvDetailView,
    InvUpdateView
)

app_name = "inventory"

urlpatterns = [
     path('manage/', InvManageView.as_view(), name="manage"),
     path('add/', InvAddView.as_view(), name="add"),
     path('delete/<pk>', InvDeleteView.as_view(), name="delete"),
     path('update/<pk>', InvUpdateView.as_view(), name="update"),
     path('detail/<slug>', InvDetailView.as_view(), name="detail"),
]