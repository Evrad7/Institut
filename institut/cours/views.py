from django.shortcuts import render, get_object_or_404
from direction.models import Cours
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def index(request):
	context={}
	context["authenticated"]=False

	if (request.user.is_authenticated and  (not request.user.is_staff)):
		nomsGroups=[group.name for group in request.user.groups.all()]
		if "etudiant" in nomsGroups:
			context["authenticated"]=True
			cours=Cours.objects.filter(specialite__pk=request.user.etudiant.specialite.pk)

			try:
				searchBy=request.GET["search-by"]
			except KeyError:
				searchBy="tous"
			try:
				search=request.GET["search"]
			except KeyError:
				search=""

			if searchBy=="titre":
				cours=cours.filter(titre__icontains=search)
			elif searchBy=="discipline":
				cours=cours.filter(discipline__icontains=search)
			elif searchBy=="auteur":
				cours=cours.filter(auteur__icontains=search)

			context["cours"]=cours


	if request.is_ajax():
		cours=list(cours.values("titre", "discipline", "auteur", "description", "support", "duree", "pk"))
		response={"cours": cours}
		return JsonResponse(response)



	return render(request, "cours/cours.html", context)

def testEtudiant(user):
	if user.is_authenticated:
		if "etudiant" in [group.name for group in user.groups.all()]:
			return True
	return False

@user_passes_test(test_func=testEtudiant)
def lireCours(request, pk_cours):
	pk_cours=int(pk_cours)
	cours=get_object_or_404(Cours, pk=pk_cours)
	return render(request, "cours/lire-cours.html", {"cours":cours})
