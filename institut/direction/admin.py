from django.contrib import admin

from .models import Etudiant, Cycle, Specialite	,Filiere, Matiere, EmploiDeTemps,\
EmploiDeTempsJounalier,  Cantine, DomaineEtude, Professeur

# Register your models here.

@admin.register(DomaineEtude)
class DomaineEtudeAdmin(admin.ModelAdmin):
	list_display=["nom"]
	fields=["nom"]
	verbose_name="domaine d'étude"



@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
	fields=["photo", "matricule", "noms", "prenoms", "date_de_naissance", "specialite", "profil"]
	list_display=["photo", "matricule", "noms", "prenoms", "date_de_naissance", "specialite", "profil", "developpment_password"]



class FiliereInline(admin.StackedInline):
	model=Filiere	
	extra=2
	verbose_name="filière"
	verbose_name_plural="filières"

	
@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
	inlines=[FiliereInline]
	list_display=["nom"]


class SpecialiteInline(admin.StackedInline):
	model=Specialite
	fields=["nom", "niveau"]


	extra=1


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
	verbose_name="filière"
	verbose_name_plural="filières"
	list_display=["nom"]
	inlines=[SpecialiteInline]
	search_fields=["nom"]
	list_filter=["cycle"]

class MatiereInline(admin.StackedInline):
	model=Matiere
	exclude=["professeur"]
	extra=1
	verbose_name="matière"
	verbose_name_plural="matières"

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
	inlines=[MatiereInline]
	verbose_name="spécialité"
	verbose_name_plural="spécialités"
	exclude=["matiere", "cours","emploi_de_temps", "delegue"]
	extra=1
	search_fields=["nom"]
	list_filter=["filiere"]


@admin.register(EmploiDeTemps)
class EmploiDeTempsAdmin(admin.ModelAdmin):
	exclude=[""]
	list_display=["en_journee", "semestre", "lundi", "mardi", "mercredi", 
	               "jeudi", "vendredi", "samedi"]
	         

@admin.register(EmploiDeTempsJounalier)
class EmploiDeTempsJounalierAdmin(admin.ModelAdmin):
	exclude=[""]

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
	exclude=[""]

