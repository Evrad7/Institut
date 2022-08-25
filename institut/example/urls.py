from django.urls import path
from .views import page


urlpatterns=[
path("page/", page, name="page")
]
