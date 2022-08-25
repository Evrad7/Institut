from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.

class Etudiant(models.Model):

	MASCULIN="MASCULIN"
	FEMININ="FEMININ"

	choices_sex=[(MASCULIN,"Masculin"), (FEMININ, "Feminin")]
	matricule=models.PositiveIntegerField(blank=True, default=0, unique=True)
	photo=models.ImageField(null=True, blank=True)
	noms=models.CharField(max_length=30)
	prenoms=models.CharField(max_length=30)
	date_de_naissance=models.DateField()
	lieu_de_naissance=models.CharField(max_length=30)
	sexe=models.CharField(max_length=10, choices=choices_sex, default=MASCULIN)
	email=models.EmailField()

	nationalite=models.CharField(default="Camerounaise", max_length=30)
	numero_CNI=models.CharField(max_length=30)
	numero_telephone=models.CharField(max_length=15, validators=[RegexValidator(
		regex=r"^(\+?\(?237\)?)?[ ]?6([ -/.]?(\d){2}){4}$", message="Mauvais format de numéro")])

	statut=models.BooleanField(default=False)
	ancienne_ecole=models.CharField(blank=True, null=True, max_length=30)
	specialite=models.ForeignKey("Specialite", on_delete=models.CASCADE)
	#absence=models.ManyToManyKey("Absence", blank=True, null=True, on_delete=models.SET_NULL)

	club=models.ForeignKey("Club", on_delete=models.CASCADE, null=True, blank=True)
	parent=models.ForeignKey("Parent", on_delete=models.SET_NULL, null=True)
	profil=models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
	cantine=models.BooleanField(default=True)
	transport=models.BooleanField(default=True)
	developpment_password=models.CharField(max_length=30)


	class Meta:
		verbose_name="Etudiant"
		verbose_name_plural="Etudiants"
	def __str__(self):
		return self.noms+" "+self.prenoms

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("direction:lire_etudiant", kwargs={"pk": self.pk})










class Note(models.Model):

	matiere=models.ForeignKey("Matiere", null=True, blank=True, on_delete=models.SET_NULL)
	sn1=models.DecimalField( max_digits=4, decimal_places=2, verbose_name="Session normale 1",
		validators=[MinValueValidator(0), MaxValueValidator(20)], null=True)
	sn2=models.DecimalField( max_digits=4, decimal_places=2, verbose_name="Session normale 2",
		validators=[MinValueValidator(0), MaxValueValidator(20)], null=True)
	cc1=models.DecimalField( max_digits=4, decimal_places=2, verbose_name="controle continu 1",
		validators=[MinValueValidator(0), MaxValueValidator(20)], null=True)
	cc2=models.DecimalField( max_digits=4, decimal_places=2, verbose_name="controle continu 2",
		validators=[MinValueValidator(0), MaxValueValidator(20)], null=True)
	etudiant=models.ForeignKey("Etudiant", null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.matiere.nom+"-"+self.etudiant.noms+" "+self.etudiant.prenoms

	class Meta:
		verbose_name="note"
		verbose_name_plural="notes"






class AbsenceEtudiant(models.Model):
	date=models.DateField()
	heure_debut=models.TimeField()
	heure_fin=models.TimeField()
	motif=models.CharField(max_length=50, null=True,)
	etudiant=models.ForeignKey("Etudiant", null=True, on_delete=models.CASCADE, related_name="absence")
	professeur=models.ForeignKey("Professeur", null=True, on_delete=models.CASCADE)


	def __str__(self):
		return "absences {}".format(self.etudiant.noms)

	class Meta:
		verbose_name="Absence de l'étudiant"
		verbose_name_plural="absences de l'étudiant"




# Pas pris en charger
class RetardEtudiant(models.Model):
	date=models.DateField()
	heure_debut=models.DateTimeField()
	heure_fin=models.DateTimeField()
	motif=models.CharField(max_length=50)
	etudiant=models.ForeignKey("Etudiant", null=True, blank=True, on_delete=models.CASCADE)


	def __str__(self):
		return "retards %s",self.etudiant

	class Meta:
		verbose_name="retard de l'étudiant"
		verbose_name_plural="retards de l'étudiant"






class AbsenceProfesseur(models.Model):
	date=models.DateField()
	heure_debut=models.TimeField()
	heure_fin=models.TimeField()
	motif=models.CharField(max_length=50, null=True)
	professeur=models.ForeignKey("Professeur", null=True, blank=True, on_delete=models.CASCADE, related_name="absence")


	def __str__(self):
		return "absences %s",self.professeur

	class Meta:
		verbose_name="Absence du professeur"
		verbose_name_plural="absences du professeur"



# Pas pris en charge
class RetardProfesseur(models.Model):
	date=models.DateField()
	heure_debut=models.DateTimeField()
	heure_fin=models.DateTimeField()
	motif=models.CharField(max_length=50)
	professeur=models.ForeignKey("Professeur", null=True, blank=True, on_delete=models.CASCADE)


	def __str__(self):
		return "retards %s",self.professeur

	class Meta:
		verbose_name="retard du professeur"
		verbose_name_plural="retards du professeur"







class Parent(models.Model):

	photo=models.ImageField(null=True, blank=True)
	noms=models.CharField(max_length=30)
	prenoms=models.CharField(max_length=30)
	email=models.EmailField(null=True, blank=True)
	date_naissance=models.DateField(null=True)
	nationalite=models.CharField(blank=True, max_length=30)
	numero_CNI=models.CharField(max_length=30)# A revoir
	profession_tuteur=models.CharField(max_length=20)
	numero_telephone=models.CharField( max_length=20, validators=[RegexValidator(
		regex=r"^(\+?\(?237\)?)?[ ]?6([ -/.]?(\d){2}){4}$", message="Mauvais format de numéro")])



	def __str__(self):
		return self.noms

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("direction:lire_parent", args=[self.pk])



	class Meta:
		verbose_name="Tuteur"
		verbose_name_plural="Tuteurs"




class Specialite(models.Model):
	nom=models.CharField(max_length=60)
	filiere=models.ForeignKey("Filiere", on_delete=models.CASCADE)
	niveau=models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)]);
	#matiere=models.ManyToManyField("Matiere",  blank=True,)
	emploi_de_temps=models.OneToOneField("EmploiDeTemps", on_delete=models.SET_NULL, null=True, blank=True)
	cours=models.ManyToManyField("Cours",blank=True)
	numero_salle=models.PositiveSmallIntegerField(validators=[MaxValueValidator(500), MinValueValidator(1)], null=True, blank=True)
	delegue=models.OneToOneField("Etudiant", related_name="delegue", on_delete=models.SET_NULL, null=True, blank=True)
	def __str__(self):
		return self.filiere.cycle.nom+"/"+self.filiere.nom+"/"+self.nom+" "+str(self.niveau)

	class Meta:
		verbose_name="Specialité"
		verbose_name_plural="Specialités"







class Matiere(models.Model):
	domaine=models.ManyToManyField("DomaineEtude")
	nom=models.CharField(max_length=70)
	programme=models.TextField(null=True, blank=True)
	credit=models.PositiveSmallIntegerField(validators=[MaxValueValidator(500), MinValueValidator(1)])
	professeur=models.ForeignKey("Professeur", on_delete=models.SET_NULL, null=True)
	specialite=models.ForeignKey("Specialite",  blank=True, on_delete=models.CASCADE, null=True)
	semestre=models.PositiveSmallIntegerField(choices=[(1, "1"), (2, "2")])

	class Meta:
		verbose_name_plural="matières"
		verbose_name="matière"

	def __str__(self):
		return self.nom


class Professeur(models.Model):
	photo=models.ImageField(null=True, blank=True)
	matricule=models.PositiveIntegerField(blank=True, default=0, unique=True)
	noms=models.CharField(max_length=30)
	prenoms=models.CharField(max_length=30)
	date_naissance=models.DateField()
	lieu_de_naissance=models.CharField(max_length=30)
	email=models.EmailField(blank=True)
	numero_telephone=models.CharField( max_length=20, validators=[RegexValidator(
		regex=r"^(\+?\(?237\)?)?[ ]?6([ -/.]?(\d){2}){4}$", message="Mauvais format de numéro")])


	domaine=models.ManyToManyField("DomaineEtude")
	nationalite=models.CharField(max_length=30, default="Camerounaise")
	numero_CNI=models.CharField(max_length=30)# A revoir

	cv=models.OneToOneField("CVProfesseur", blank=True, null=True, on_delete=models.SET_NULL)
	emploi_de_temps=models.OneToOneField("EmploiDeTemps", blank=True, null=True, on_delete=models.SET_NULL)
	profil=models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
	developpment_password=models.CharField(max_length=30)




	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("direction:lire_professeur", args=[self.pk])

	def __str__(self):
		return self.noms+" "+self.prenoms

	class Meta:
		verbose_name="Professeur"
		verbose_name_plural="Professeurs"


class DomaineEtude(models.Model):
	nom=models.CharField(max_length=30)
	def __str__(self):
		return self.nom




class CVProfesseur(models.Model):
	nom_diplomes=models.CharField(max_length=30)
	annee_obtension_diplome=models.CharField(max_length=4,  validators=[RegexValidator(
		regex=r"^\d{4}$", message="année invalide")])
	ecole_obtension_diplome=models.CharField(max_length=30)

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("direction:lire_cv", args=[self.pk])




class EmploiDeTemps(models.Model):
	en_journee=models.BooleanField(default=True)
	semestre=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2)],default=1)
	lundi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="lundi", verbose_name="lundi")
	mardi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="mardi", verbose_name="mardi")
	mercredi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="mercredi", verbose_name="mercredi")
	jeudi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="jeudi",verbose_name="jeudi")
	vendredi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="vendredi", verbose_name="vendredi")
	samedi=models.OneToOneField("EmploiDeTempsJounalier", on_delete=models.SET_NULL, null=True, blank=True, related_name="samedi", verbose_name="samedi")


class EmploiDeTempsJounalier(models.Model):

	periode1=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode1")
	periode2=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode2")
	periode3=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode3")
	periode4=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode4")
	periode5=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode5")
	periode6=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode6")
	periode7=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode7")
	periode8=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode8")
	periode9=models.ForeignKey("Matiere", blank=True, null=True, on_delete=models.SET_NULL, related_name="periode9")





class Filiere(models.Model):
	nom=models.CharField(max_length=30)
	cycle=models.ForeignKey("Cycle", on_delete=models.CASCADE)

	#programme=models.FileField(blank=True, null=True)
	#cours=models.FileField(blank=True, null=True)

	def __str__(self):
		return self.nom

	class Meta:
		verbose_name="Filière"
		verbose_name_plural="Filières"

class Cycle(models.Model):
	nom=models.CharField(max_length=30)
	diplome=models.CharField(max_length=30)
	langue=models.CharField(max_length=2, choices=[("FR", "Français"), ("EN", "Anglais")], default="FR")

	def __str__(self):
		return self.nom

	class Meta:
		verbose_name="cycle"
		verbose_name_plural="cycles"



class Club(models.Model):
	nom=models.CharField(max_length=30)
	delegue_club=models.ForeignKey("Etudiant", on_delete=models.SET_NULL, null=True, related_name="delegue_club")
	planning_des_activités=models.FileField(max_length=30, null=True, blank=True)

	def __str__(self):
		return self.nom

	class Meta:
		verbose_name="Club"
		verbose_name_plural="Clubs"


class Cantine(models.Model):
	image=models.ImageField(null=True, blank=True)
	noms=models.CharField(max_length=30)
	prenoms=models.CharField(max_length=30)
	nationalite=models.CharField(max_length=30)
	numero_telephone=models.PositiveSmallIntegerField(validators=[RegexValidator(
		regex=r"^(\+?(237))?[ -/.]6?([ -/.](\d){2}){4}$", message="Mauvais format de numéro")])

	email=models.EmailField()
	menu=models.OneToOneField("MenuCantine", blank=True, null=True, on_delete=models.SET_NULL)

	class Meta:
		verbose_name="Cantine"
		verbose_name_plural="Cantines"
	def __str__(self):
		return "cantine"

class MenuCantine(models.Model):
	petit_dejeuner=models.CharField(max_length=30, verbose_name="le petit dejeuner de chaque jour")
	image_petit_dejeuner=models.ImageField(blank=True, null=True,verbose_name="image du petit dejeuner")
	image_lundi=models.ImageField(blank=True, null=True  ,verbose_name="image du menu dejeuner Lundi ")
	image_mardi=models.ImageField(blank=True, null=True , verbose_name="image du menu dejeuner Mardi")
	image_mercredi=models.ImageField(null=True , verbose_name="image du menu dejeuner Mercredi")
	image_jeudi=models.ImageField(blank=True, null=True , verbose_name="image du menu dejeuner Jeudi")
	image_vendredi=models.ImageField(blank=True, null=True , verbose_name="image du menu dejeuner Vendredi")
	image_samedi=models.ImageField(blank=True, null=True , verbose_name="image du menu dejeuner Samedi ")
	lundi=models.CharField(max_length=30, verbose_name="menu dejeuner du Lundi")
	mardi=models.CharField(max_length=30, verbose_name="menu dejeuner du Mardi")
	mercredi=models.CharField(max_length=30, verbose_name="menu dejeuner du Mercredi")
	jeudi=models.CharField(max_length=30, verbose_name="menu dejeuner du Jeudi")
	vendredi=models.CharField(max_length=30, verbose_name="menu dejeuner du Vendredi")
	samedi=models.CharField(max_length=30, verbose_name="menu dejeuner du Samedi")

	def __str__(self):
		return "menu de la cantine"

	class Meta:
		verbose_name="menu de la cantine"



class Transport(models.Model):
	noms=models.CharField(max_length=30)
	prenoms=models.CharField(max_length=30)
	image=models.ImageField(null=True, blank=True)
	debut_matin=models.TimeField(null=True, blank=True ,verbose_name="début de l'heure de passage du bus le matin")
	fin_matin=models.TimeField(null=True, blank=True, verbose_name="fin de l'heure de passage du bus le matin")
	debut_soir=models.TimeField(null=True, blank=True, verbose_name="début de l'heure de passage du bus le soir")
	fin_soir=models.TimeField(null=True, blank=True, verbose_name="fin de l'heure de passage du bus le soir")


	def __str__(self):
		return "transport"

	class Meta:
		verbose_name="transport"

class Cours(models.Model):
	titre=models.CharField(max_length=30)
	discipline=models.CharField(max_length=30)
	auteur=models.CharField(max_length=30)
	description=models.CharField(max_length=100)
	support=models.CharField(max_length=10)
	duree=models.PositiveSmallIntegerField()
	support_cours=models.FileField()

	def __str__(self):
		return "{}__{}".format(self.titre, self.auteur)

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("direction:lire_cours", kwargs={"pk":self.pk})
	class Meta:
		verbose_name="Cours"


class Blog(models.Model):
	vidoes=models.FileField(null=True, blank=True)
	image=models.ImageField(null=True, blank=True)
	titre=models.CharField(max_length=30)
	contenu=models.TextField()
	auteur=models.CharField(max_length=30)
	date_publication=models.DateField(auto_now_add=True)



	def __str__(self):
		return "%s_%s", self.titre, self.auteur
