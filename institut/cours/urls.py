from django.urls import path
from . import views



urlpatterns=[
	path("", views.index, name="index"),
	path("lire_cours/<int:pk_cours>/", views.lireCours, name="lire_cours"),
]
