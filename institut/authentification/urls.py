from django.urls import path
from .views import  loginView
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path("login/", loginView, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
