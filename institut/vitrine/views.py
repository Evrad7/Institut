from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, F
from django.template import loader
from vitrine.models import Partenaire
from direction.models import Specialite, Filiere, Cycle

# Create your views here.


def index(request):
	partenaires=Partenaire.objects.all()
	return render(request, "vitrine/index.html", {"partenaires":partenaires})

def inscription(request):
	if request.is_ajax():


		try:
			search=request.GET["search"]
		except:
			search=None
		try:
			pk_filiere=request.GET["filiere"]
			pk_filiere=int(pk_filiere)
			filiere=Filiere.objects.get(pk=pk_filiere)
			if search is not None:
				print(filiere)
				specialites=Specialite.objects.filter(Q(filiere=filiere)&Q(nom__icontains=search))
			else:
				print(filiere)
				specialites=Specialite.objects.filter(filiere=filiere)

		except:
			try:
				pk_cycle=request.GET["cycle"]
				pk_cycle=int(pk_cycle)
				cycle=Cycle.objects.get(pk=pk_cycle)
				if search is not None:
					specialites=Specialite.objects.filter(Q(filiere__cycle=cycle)&Q(nom__icontains=search))
				else:
					specialites=Specialite.objects.filter(filiere__cycle=cycle)
			except:
				if search is not None:
					specialites=Specialite.objects.filter(nom__icontains=search)
				else:
					specialites=Specialite.objects.all()



		specialites=specialites.annotate(nom_filiere=F("filiere__nom"), nom_cycle=F("filiere__cycle__nom"))
		specialites=list(specialites.values("nom", "niveau", "nom_filiere",  "nom_cycle"))

		response={"specialites":specialites}

		return JsonResponse(response)

	context={}
	specialites=Specialite.objects.all()
	filieres=Filiere.objects.all()
	cycles=Cycle.objects.all()
	partenaires=Partenaire.objects.all()
	context["partenaires"]=partenaires
	context["specialites"]=specialites
	context["filieres"]=filieres
	context["cycles"]=cycles

	return render(request, "vitrine/inscription.html", context)


def vieEtudiantine(request):
	return render(request, "vitrine/vie_etudiantine.html", {})

def propos(request):
	partenaires=Partenaire.objects.all()
	return render(request, "vitrine/propos.html", {"partenaires":partenaires})


def contact(request):
	return render(request, "vitrine/contacter.html",  {})
