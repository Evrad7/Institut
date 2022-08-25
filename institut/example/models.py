from django.db import models

# Create your models here.

class Jeu(models.Model):
    nom=models.CharField(max_length=30)
    type=models.CharField(max_length=30)
    taille=models.CharField(max_length=10)
    prix=models.PositiveIntegerField()
