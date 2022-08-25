from django.shortcuts import render, redirect
from django.urls import reverse
#from django.contrib.auth.views import LogoutView
#from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.

def loginView(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(request, username=username, password=password)
            if user:

                login(request, user)
                if user.is_staff:
                    return redirect(reverse("direction:acceuil"))
                nomsGroups=[group.name for group in user.groups.all()]


                if "etudiant" in nomsGroups:
                    if user.etudiant.specialite.delegue.pk==user.etudiant.pk:
                        request.session["pk_delegue"]=user.etudiant.pk
                        return redirect(reverse("direction:acceuil"))
                    return redirect(reverse("cours:index"))
                elif "professeur" in nomsGroups:
                    request.session["pk_professeur"]=user.professeur.pk
                    return(redirect(reverse("direction:acceuil")))
                elif  "directeur académique" in nomsGroups:
                    return redirect(reverse("direction:acceuil"))
                elif  "secrétaire professeur" in nomsGroups:
                    return redirect(reverse("direction:acceuil"))


                return redirect(reverse("vitrine:index"))
            else:
                form.errors["__all__"]=" La correspondance pseudonyme-mot de passe est invalide"
                return render(request, "authentification/login.html", locals() )
        else:
            return render(request, "authentification/login.html", {"form":form})
    else:
        form=LoginForm()
        return render(request, "authentification/login.html", locals())
