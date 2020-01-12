from django.urls import path, include
from .views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
     path('login', LoginView.as_view(), name="login"),
     path('logout', LogoutView.as_view(), name="logout"),
]