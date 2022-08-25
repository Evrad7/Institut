from django.contrib import admin
from .models import Jeu

# Register your models here.

@admin.register(Jeu)
class JeuAdmin(admin.ModelAdmin):
    exclude=[""]
