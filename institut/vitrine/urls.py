
from django.urls import path
from .import views



urlpatterns=[
	path("index/", views.index, name="index"),
	path("inscription/", views.inscription, name="inscription"),
	path("vie_etudiantine/", views.vieEtudiantine, name="vie_etudiantine"),
	path("propos/", views.propos, name="propos"),
	path("cantact/", views.contact, name="contact"),
]