from django.db import models

# Create your models here.

class Partenaire(models.Model):
    nom=models.CharField(max_length=60)
    description=models.TextField()
