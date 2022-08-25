from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from .forms import InscriptionForm, AjoutParentForm, RechercheForm,\
ParagraphErrorList,     AjoutEtudiantForm, InscriptionAncienEtudiantForm,\
AjoutProfesseurForm, AjoutCVForm, EmploiDeTempsForm, AjoutCoursForm, AbsenceEtudiantForm,\
AbsenceProfesseurForm
from .models import Etudiant, Parent, Cycle, Filiere, Specialite, Professeur,\
CVProfesseur, EmploiDeTemps as Emploi, EmploiDeTempsJounalier,  Matiere, DomaineEtude,\
Cours, Note, AbsenceEtudiant, AbsenceProfesseur
from django.db.models import Q, F, Sum
import datetime
from django.http import Http404, JsonResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from .utils import getPassword
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.


def testToManage(user):#TestSecretaireEtudiant
    try:
        group=user.groups.get(name="secretaire etudiant")
        return True
    except:
        return False

def testProfesseur(user):
    try:
        group=user.groups.get(name="professeur")
        return True
    except:
        return False

def testDelegue(user):
    try:
        group=user.groups.get(name="etudiant")
        if user.etudiant.specialite.delegue.pk==user.etudiant.pk:
            return True
        return False
    except:
        return False

def testSecretaireProfesseur(user):
    try:
        group=user.groups.get(name="secrétaire professeur")
        return True
    except:
        return False


def testDirecteurAcademique(user):
    try:
        group=user.groups.get(name="directeur académique")
        return True
    except:
        return False


def testToSeeIndex(user):
    try:
        group=user.groups.get(name="professeur")
        return True
    except:
        try:
            group=user.groups.get(name="secretaire etudiant")
            return True
        except:
            try:
                group=user.groups.get(name="etudiant")
                if user.etudiant.specialite.delegue.pk==user.etudiant.pk:
                    return True
                return False
            except:
                try:
                    group=user.groups.get(name="directeur académique")
                    return True
                except:
                    try:
                        group=user.groups.get(name="secrétaire professeur")
                        return True
                    except:
                        return False
                    return False


LOGIN_URL_PASSES_TEST="/vitrine/index/"
LOGIN_URL_TEST_PROFESSEUR="/vitrine/index/"



@user_passes_test(test_func=testToSeeIndex, login_url=LOGIN_URL_PASSES_TEST)
def index(request):
    return render(request, "direction/acceuil.html", {"title": "Etudiants"})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def etudiant(request):
    return render(request, "direction/etudiant.html", {"title":"gestion des etudiants"})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def professeur(request):
    return render(request, "direction/professeurs.html", {})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def parent(request):
    return render(request, "direction/parent.html", {})


def professeur(request):
    return render(request, "direction/professeur.html", {})

#@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def parametre(request):
   return render(request, "direction/parametre.html", {})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def quitter(request):
    return redirect(reverse("vitrine:index"))




@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def inscription(request, old=None):
    prev="/direction/etudiant/"

    if old=='0':
        return redirect("/direction/parent/ajout_parent")
    elif  old=='1':
        return redirect(reverse("direction:recherche_ancien_etudiant", args=[1]))

    else:
        return render(request, "direction/inscription.html", {"prev":prev})




@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def ajoutAncienEtudiant(request):
    pass

@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def rechercheAncienEtudiant(request, next_):
    #next_==4:echange_parent
    progression=True
    if (next_==2 or next_==3 ):
        progression=False
        prev="/direction/etudiant/"
    elif next_==4:
        progression=False
        prev="/direction/parent/"
    else:
        prev="/direction/etudiant/inscription/None"


    errors_={}
    if request.method=="POST":
        form=RechercheForm(request.POST)

        if form.is_valid():
            matricule=form.cleaned_data["matricule"]
            nom=form.cleaned_data["nom"]
            prenom=form.cleaned_data["prenom"]

            if matricule:
                try:
                    etudiant=Etudiant.objects.get(matricule=matricule)
                    if next_==2:
                        return redirect(reverse("direction:modification_etudiant", args=[etudiant.pk]))
                    elif next_==3:
                        return redirect(reverse("direction:suppression_etudiant",args=[etudiant.pk]))
                    elif next_==4:
                        return redirect(reverse("direction:echange_parent", args=[etudiant.pk]))

                    return redirect(reverse("direction:inscription_ancien_etudiant", args=[etudiant.pk]))

                except Etudiant.DoesNotExist:
                    errors_["error-matricule"]="le matricule est incorrect"
            else:
                if not prenom:
                    etudiants=Etudiant.objects.filter(noms=nom)
                else:
                    etudiants=Etudiant.objects.filter(Q(noms=nom)& Q(prenoms=prenom))
                if len(etudiants)==1:
                    etudiant=etudiants[0]

                    if next_==2:
                        return redirect(reverse("direction:modification_etudiant", args=[etudiant.pk]))
                    elif next_==3:
                        return redirect(reverse("direction:suppression_etudiant" ,args=[etudiant.pk]))
                    elif next_==4:
                        return redirect(reverse("direction:echange_parent", args=[etudiant.pk]))


                    return redirect(reverse("direction:inscription_ancien_etudiant", args=[etudiant.pk]))

                errors_["empty"]="Aucun étudiant trouvé "

            return render(request, "direction/recherche-ancien-etudiant.html", {"form": form, "errors_":errors_.values(), "prev":prev,  "progression":progression})


        return render(request, "direction/recherche-ancien-etudiant.html", {"form": form, "prev":prev,  "progression":progression})




    form=RechercheForm()
    return render(request, "direction/recherche-ancien-etudiant.html", {"form": form,"prev":prev, "progression":progression})
@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def ajoutParent(request):
    #request.session.flush()
    try:
        prev=request.GET["prev"]
    except:
        prev="/direction/etudiant/inscription/None/"

    if request.method=="POST":

        form=AjoutParentForm(request.POST, request.FILES,  error_class=ParagraphErrorList)
        if form.is_valid():
            data=form.cleaned_data
            data["date_naissance"]=data["date_naissance"].strftime("%Y-%m-%d")
            request.session["parent"]=data
            prev_=request.path
            return redirect("/direction/etudiant/ajout_etudiant")
        return render(request, "direction/ajout-parent.html/", {"form":form, "prev":prev})


    if "parent" in request.session:
        parent=request.session["parent"]
        parent["date_naissance"]=datetime.datetime.strptime(parent["date_naissance"], "%Y-%m-%d").date()

    else:
        parent=None


    form=AjoutParentForm(initial=parent)
    return render(request, "direction/ajout-parent.html", {"form":form, "prev":prev})


def ajoutEtudiant(request):

    prev="/direction/parent/ajout_parent/"
    try:
        data=request.session["parent"]
        data["date_naissance"]=datetime.datetime.strptime(data["date_naissance"], "%Y-%m-%d").date()

        parent=True
    except KeyError:
        parent=False
    if (request.method=="POST") & (parent==True):
        form=AjoutEtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            parent=Parent.objects.create(
                        photo=data["photo"],
                        noms=data["noms"],
                        prenoms=data["prenoms"],
                        email=data["email"],
                        date_naissance=data["date_naissance"],
                        nationalite=data["nationalite"],
                        numero_CNI=data["numero_CNI"],
                        profession_tuteur=data["profession_tuteur"],
                        numero_telephone=data["numero_telephone"]
                         )
            etudiant=form.save(commit=False)
            etudiant.parent=parent
            del request.session["parent"]
            etudiant.developpment_password=getPassword(10)
            etudiant.save()
            etudiant.matricule=etudiant.id
            etudiant.statut=True
            username=etudiant.prenoms.split(" ")[0]
            username="{0}_{1}".format(username, str(etudiant.pk))
            group=Group.objects.get(name="etudiant")


            #send mail here---------------------------------------

            profil=User.objects.create_user(username=username, password=etudiant.developpment_password, email=etudiant.email, first_name=etudiant.noms,
                last_name=etudiant.prenoms)
            profil.user_permissions.clear()
            profil.groups.add(group)

            profil.save()
            etudiant.profil=profil
            etudiant.save()

            return render(request, "direction/acceuil.html", {"inscription-reussi": True})

        return render(request, "direction/ajout-etudiant.html", {"form": form, "parent":parent, "prev":prev})


    form=AjoutEtudiantForm()
    return render(request, "direction/ajout-etudiant.html", {"form":form, "parent":parent, "prev":prev})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def modificationEtudiant(request):
    return render(request, "direction/modification-etudiant.html", {})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def inscriptionAcienEtudiant(request, matricule):
    prev="direction:recherche_ancien_etudiant"
    etudiant=get_object_or_404(Etudiant, matricule=matricule)
    if request.method=="POST":
        form=InscriptionAncienEtudiantForm(request.POST, request.FILES, error_class=ParagraphErrorList)
        if form.is_valid():
            #if form.cleaned_data["photo"]!=etudiant.photo:
                #form.errors["tml"]="Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["photo"].label
            form.errors["tml"]=""
            if form.cleaned_data["noms"]!=etudiant.noms:
                form.errors["tml"]+="Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["noms"].label
            if form.cleaned_data["prenoms"]!=etudiant.prenoms:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["prenoms"].label
            if form.cleaned_data["lieu_de_naissance"]!=etudiant.lieu_de_naissance:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["lieu_de_naissance"].label
            if form.cleaned_data["sexe"]!=etudiant.sexe:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["sexe"].label
            if form.cleaned_data["nationalite"]!=etudiant.nationalite:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["nationalite"].label
            if form.cleaned_data["numero_CNI"]!=etudiant.numero_CNI:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["numero_CNI"].label
            if form.cleaned_data["numero_telephone"]!=etudiant.numero_telephone:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["numero_telephone"].label
            if form.cleaned_data["email"]!=etudiant.email:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["email"].label
            if form.cleaned_data["ancienne_ecole"]!=etudiant.ancienne_ecole:
                form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["ancienne_ecole"].label
            if form.cleaned_data["date_de_naissance"]!=etudiant.date_de_naissance:
               form.errors["tml"]+="<br/>Vous n'êtes pas autorisé à modifier le champ %s"%form.fields["date_de_naissance"].label

            if form.errors["tml"]!="":
                form.errors["tml"]=mark_safe(form.errors["tml"])
                return render(request, "direction/inscription-ancien-etudiant.html", {"form":form, "prev":prev})



            return redirect(reverse("direction:acceuil"))
        form.instance=None
        return render(request, "direction/inscription-ancien-etudiant.html", {"form":form, "prev":prev})

    etudiant=get_object_or_404(Etudiant, matricule=matricule)
    form=InscriptionAncienEtudiantForm(instance=etudiant)

    return render(request, "direction/inscription-ancien-etudiant.html", {"form":form, "prev":prev})



class ListeEtudiant(UserPassesTestMixin, ListView):
    template_name="direction/liste-etudiant.html"
    model=Etudiant
    context_object_name="etudiants"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context["filtre_cycle"]=Cycle.objects.all()
        filtre_specialite=Specialite.objects.all()
        filtre_specialite=([{"nom":s.nom, "niveau":s.niveau, "pk":s.pk} for s in filtre_specialite])
        filtre_specialite.sort(key=lambda x:(x["nom"], x["niveau"]))
        context["filtre_specialite"]=filtre_specialite
        context["filtre_filiere"]=Filiere.objects.all()
        context["option_search"]=["Matricules","Noms et/ou Prenoms", "Specialites", "Filieres"]
        try:
            pk=self.request.GET["specialite"]
            pk=int(pk)
            context["active_specialite"]=pk
            return context
        except:
            pass

        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            context["active_cycle"]=pk
            return context
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            context["active_filiere"]=pk

            return context
        except:
            pass

        return context

    def get_queryset(self, **kwargs):
        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            return Etudiant.objects.filter(specialite__filiere__cycle_id=pk).order_by("-matricule")
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            return Etudiant.objects.filter(specialite__filiere_id=pk).order_by("-matricule")
        except:
            pass

        try:
            pk=self.request.GET["specialite"]
            pk=int(pk)
            return Etudiant.objects.filter(specialite_id=pk).order_by("-matricule")
        except:
            pass

        try:
            searchBy=self.request.GET["search-by"]
            search=self.request.GET["search"]
            if searchBy=="Matricules":
                try:
                    matricule=int(search)
                except ValueError:
                    return []

                return Etudiant.objects.filter(matricule=matricule)
            if searchBy=="Noms et/ou Prenoms":
                return Etudiant.objects.filter(Q(noms__icontains=search) | Q(prenoms__icontains=search)).order_by("-matricule")
            if searchBy=="Specialites":
                return Etudiant.objects.filter(specialite__nom__icontains=search).order_by("-matricule")
            if searchBy=="Filieres":
                return Etudiant.objects.filter(specialite__filiere__nom__icontains=search).order_by("-matricule")
        except:
            pass


        etudiants=Etudiant.objects.all().order_by("-matricule")
        return etudiants


class LireEtudiant(UserPassesTestMixin, DetailView):
    template_name="direction/lire-etudiant.html"
    model=Etudiant
    context_object_name="etudiant"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False

class ModificationEtudiant(UserPassesTestMixin, UpdateView):

    template_name="direction/modification-etudiant.html"
    model=Etudiant
    form_class=AjoutEtudiantForm
    context_object_name="etudiant"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False


class SuppressionEtudiant(UserPassesTestMixin, DeleteView):
    template_name="direction/suppression-etudiant.html"
    model=Etudiant
    context_object_name="etudiant"
    success_url="/direction/etudiant/liste_etudiant/"
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False

@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def insertionParent(request, choice):
    if choice==1:
        return redirect(reverse("direction:inscription", args=[None]))
    if choice==2:
        return redirect(reverse("direction:recherche_ancien_etudiant", kwargs={"next_":4}))
    prev=reverse("direction:parent")
    return render(request, "direction/insertion-parent.html", {"prev":prev})


@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def echangeParent(request, matricule):
    prev=reverse("direction:recherche_ancien_etudiant", args=[4])
    etudiant=get_object_or_404(Etudiant, matricule=matricule)
    form=AjoutParentForm(error_class=ParagraphErrorList)
    if request.method=="POST":
        form=AjoutParentForm(request.POST, request.FILES, error_class=ParagraphErrorList)
        if form.is_valid():
            etudiant.parent=form.instance
            form.save()
            etudiant.save()
            pk_parent=etudiant.parent.pk
            return redirect(reverse("direction:lire_parent" , args=[pk_parent]))

    return render(request, "direction/echange-parent.html", {"form": form, "etudiant": etudiant, "prev": prev})


class ListeParent(UserPassesTestMixin ,ListView):
    template_name="direction/liste-parent.html"
    model=Parent
    context_object_name="parents"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["option_search"]={"n":"noms et/ou prénoms",
                           "pr": "profession du tuteur", "m":"matricule de l'étudiant"}

        return context

    def get_queryset(self):

        try:
            nb=self.request.GET["nb"]
            nb=int(nb)
            if nb<1:
                nb=15
        except:
            nb=15

        try:
            searchBy=self.request.GET["search-by"]
            search=self.request.GET["search"]


            if searchBy=="n":
                return Parent.objects.filter(Q(noms__icontains=search) | Q(prenoms__icontains=search)).order_by("-pk")[:nb]
            if searchBy=="pr":
                return Parent.objects.filter(profession_tuteur__icontains=search).order_by("-pk")[:nb]
            if searchBy=="m":
                matricule=int(search)
                return Parent.objects.filter(etudiant__matricule=matricule).order_by("-pk")[:nb]
        except:
            return Parent.objects.all().order_by("-pk")[:nb]



@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def rechercheParent(request):
    prev=reverse("direction:parent")
    errors_={}
    if request.method=="POST":
        form=RechercheForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            matricule=form.cleaned_data["matricule"]
            nom=form.cleaned_data["nom"]
            prenom=form.cleaned_data["prenom"]

            if matricule:
                try:
                    parent=Parent.objects.get(etudiant__matricule=matricule)

                    return redirect("/direction/parent/modification_parent/%s/?prev=/direction/parent/recherche_parent/" %parent.pk)
                except Parent.DoesNotExist:
                    errors_["error-matricule"]="Le matricule est incorrect"
            else:
                if not prenom:
                    parents=Parent.objects.filter(noms=nom)
                else:
                    parents=Parent.objects.filter(Q(noms=nom)& Q(prenoms=prenom))
                if len(parents)==1:
                    parent=parents[0]
                    return redirect("/direction/parent/modification_parent/%s/?prev=/direction/parent/recherche_parent/" %parent.pk)


                errors_["empty"]="Aucun parent trouvé "

        return render(request, "direction/recherche-parent.html", {"form": form, "errors_":errors_.values(), "prev":prev})

    form=RechercheForm()
    return render(request, "direction/recherche-parent.html", {"form":form, "prev": prev})



class ModificationParent(UserPassesTestMixin ,UpdateView):
    template_name="direction/modification-parent.html"
    model=Parent
    form_class=AjoutParentForm
    context_object_name="parent"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        try:
            context["prev"]=self.request.GET["prev"]
        except:
            pass
        return context

class LireParent(UserPassesTestMixin ,DetailView):
    model=Parent
    template_name="direction/lire-parent.html"
    context_object_name="parent"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secretaire etudiant")
            return True
        except:
            return False



@user_passes_test(test_func=testToManage, login_url=LOGIN_URL_PASSES_TEST)
def suppressionParent(request):

    return render(request, "direction/suppression-parent.html", {})


def ajoutProfesseur(request):
    try:
        prev=request.GET["prev"]
    except KeyError:
        prev=reverse("direction:professeur")

    if request.method=="POST":
        form=AjoutProfesseurForm(request.POST, request.FILES,error_class=ParagraphErrorList)
        if form.is_valid():

            professeur=form.save(commit=False)
            professeur.developpment_password=getPassword(10)
            professeur.save()
            form.save_m2m()
            username=professeur.prenoms.split(" ")[0]
            username="prof_{}_{}".format(username, professeur.pk)
            profil=User.objects.create_user(username=username, email=professeur.email,
             password=professeur.developpment_password, first_name=professeur.prenoms,
             last_name=professeur.noms)

            group=Group.objects.get(name="professeur")
            profil.groups.add(group)
            profil.save()
            professeur.matricule=professeur.pk
            professeur.profil=profil
            professeur.save()

            return redirect(reverse("direction:ajout_cv", kwargs={"pk":professeur.pk}))

        return render(request, "direction/ajout-professeur.html", {"form": form, "prev":prev})

    form=AjoutProfesseurForm()
    return render(request, "direction/ajout-professeur.html", {"form":form, "prev": prev})


def ajoutCV(request, pk):

    professeur=get_object_or_404(Professeur, pk=pk)
    if request.method=="POST":
        form=AjoutCVForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            cv=form.save()
            professeur.cv=cv
            professeur.save()
            return redirect(reverse("direction:liste_professeur"))
        return render(request, "direction/ajout-cv.html", {"form":form, "noms":professeur.noms, "prenoms":professeur.prenoms,"pk": pk})
    form=AjoutCVForm()
    return render(request, "direction/ajout-cv.html", {"form":form, "noms":professeur.noms, "prenoms":professeur.prenoms, "pk":pk})


class ListeProfesseur(UserPassesTestMixin, ListView):
    template_name="direction/liste-professeur.html"
    context_object_name="professeurs"
    model=Professeur

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secrétaire professeur")
            return True
        except:
            return False



    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["filtre_cycle"]=Cycle.objects.all()
        filtre_specialite=Specialite.objects.all()
        filtre_specialite=([{"nom":s.nom, "niveau":s.niveau, "pk":s.pk} for s in filtre_specialite])
        filtre_specialite.sort(key=lambda x:(x["nom"], x["niveau"]))
        context["filtre_specialite"]=filtre_specialite
        context["filtre_filiere"]=Filiere.objects.all()
        context["option_search"]=["Matricules","Noms et/ou Prenoms", "Specialites", "Filieres"]
        try:
            pk=self.request.GET["specialite"]
            pk=int(pk)
            context["active_specialite"]=pk
            return context
        except:
            pass

        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            context["active_cycle"]=pk
            return context
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            context["active_filiere"]=pk

            return context
        except:
            pass

        return context

    def get_queryset(self):
        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            cycle=Cycle.objects.get(pk=pk)
            professeurs=[]
            for filiere in cycle.filiere_set.all():
                for specialite in filiere.specialite_set.all():
                    for matiere in specialite.matiere:
                        professeurs.append(matiere.professeur)

            professeurs.sort(key=lambda x:x.pk, reverse=True)
            return professeurs
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            filiere=Filiere.objects.get(pk=pk)
            professeurs=[]
            for specialite in filiere.specialite_set.all():
                for matieres in specialite.matiere.all():
                    for matiere in matieres:
                        professeurs.append(matiere.professeur)

            professeurs.sort(key=lambda x:x.pk, reverse=True)
            return professeurs
        except:
            pass

        try:
            pk=self.request.GET["specialite"]
            pk=int(pk)
            specialite=Specialite.objects.get(pk=pk)
            professeurs=[]
            for matiere in specialite.matiere.all():
                professeurs.append(matiere.professeur)

            professeurs.sort(key=lambda x:x.pk, reverse=True)
            return professeurs
        except:
            pass


        try:
            searchBy=self.request.GET["search-by"]
            search=self.request.GET["search"]
            if searchBy=="Matricules":
                try:
                    matricule=int(search)
                except ValueError:
                    return []

                return Professeur.objects.filter(matricule=matricule)
            if searchBy=="Noms et/ou Prenoms":
                return Professeur.objects.filter(Q(noms__icontains=search) | Q(prenoms__icontains=search)).order_by("-matricule")
            if searchBy=="Specialites":
                specialites=Specialite.objects.filter(nom__icontains=search)
                professeurs=[]
                for specialite in specialites:
                    for matiere in specialite.matiere:
                        professeurs.append(matiere.professeur)
                professeurs.sort(key=lambda x:x.pk, reverse=True)
                return professeurs

            if searchBy=="Filieres":
                filieres=Filiere.objects.filter(nom__icontains=search)
                professeurs=[]
                for filiere in filieres:
                    for specialite in filiere.specialite_set.all():
                        for matiere in specialite.matiere:
                            professeurs.append(matiere.professeur)
                professeurs.sort(key=lambda x:x.pk, reverse=True)
                return professeurs

        except:
            pass


        professeurs=Professeur.objects.all().order_by("-matricule")
        return professeurs

class LireProfesseur(UserPassesTestMixin, DetailView):
    model=Professeur
    template_name="direction/lire-professeur.html"
    context_object_name="professeur"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secrétaire professeur")
            return True
        except:
            return False


class ModificationProfesseur(UserPassesTestMixin, UpdateView):
    model=Professeur
    template_name="direction/modification-professeur.html"
    form_class=AjoutProfesseurForm
    context_object_name="professeur"
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secrétaire professeur")
            return True
        except:
            return False

class SuppressionProfesseur(UserPassesTestMixin, DeleteView):
    model=Professeur
    template_name="direction/suppression-professeur.html"
    context_object_name="professeur"
    success_url="/direction/professeur/liste_professeur/"
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="secrétaire professeur")
            return True
        except:
            return False



@user_passes_test(test_func=testSecretaireProfesseur, login_url=LOGIN_URL_PASSES_TEST)
def rechercheProfesseur(request, next_):
    prev=reverse("direction:professeur")
    errors_={}
    #next_=0=>Suppression du professeur
    #next_=1=>Modification du professeur
    if (next_==0) or (next_==1):
        pass
    else:
        raise Http404()

    if request.method=="POST":
        form=RechercheForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            matricule=form.cleaned_data["matricule"]
            nom=form.cleaned_data["nom"]
            prenom=form.cleaned_data["prenom"]

            if matricule:
                try:
                    professeur=Professeur.objects.get(matricule=matricule)
                    if next_==0:
                        return redirect("/direction/professeur/suppression_professeur/%s/?prev=/direction/professeur/recherche_professeur/0/"%professeur.pk)
                    else:
                        return redirect("/direction/professeur/modification_professeur/%s/?prev=/direction/professeur/recherche_professeur/1/"%professeur.pk)

                except Professeur.DoesNotExist:
                    errors_["error-matricule"]="Le matricule est incorrect"
            else:
                if not prenom:
                    professeurs=Professeur.objects.filter(noms=nom)
                else:
                    professeurs=Professeur.objects.filter(Q(noms=nom)& Q(prenoms=prenom))
                if len(professeurs)==1:
                    professeur=professeurs[0]
                    if next_==0:
                        return redirect("/direction/professeur/suppression_professeur/%s/?prev=/direction/professeur/recherche_professeur/0/"%professeur.pk)
                    else:
                        return redirect("/direction/professeur/modification_professeur/%s/?prev=/direction/professeur/recherche_professeur/1/"%professeur.pk)

                errors_["empty"]="Aucun parent trouvé "


        return render(request, "direction/recherche-professeur.html", {"form": form, "errors_":errors_.values(), "prev":prev})
    form=RechercheForm()
    return render(request, "direction/recherche-professeur.html", {"form": form, "prev":prev})


class ModificationCV(UserPassesTestMixin, UpdateView):
    template_name="direction/modification-cv.html"
    model=CVProfesseur
    form_class=AjoutCVForm
    context_object_name="cv"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="directeur académique")
            return True
        except:
            return False

class LireCV(UserPassesTestMixin, DetailView):
    template_name="direction/lire-cv.html"
    model=CVProfesseur
    context_object_name="cv"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="directeur académique")
            return True
        except:
            return False

#AjoutCycle, SuppressionCycle, ModificationCycle, LireCycle,\
#ListeCycle

class EmploiDeTemps(UserPassesTestMixin, ListView):


    template_name="direction/emploi-de-temps.html"
    model=Specialite
    context_object_name="specialites"

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="directeur académique")
            return True
        except:
            return False


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["filtre_cycle"]=Cycle.objects.all()
        context["filtre_filiere"]=Filiere.objects.all()
        context["option_search"]=["Matricules","Noms et/ou Prenoms", "Specialites", "Filieres"]

        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            context["active_cycle"]=pk
            return context
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            context["active_filiere"]=pk

            return context
        except:
            pass

        try:
            search=self.request.GET["search"]
            context["search"]=search
        except:
            pass

        return context

    def get_queryset(self):



        try:
            pk=self.request.GET["cycle"]
            pk=int(pk)
            specialites=Specialite.objects.filter(filiere__cycle__pk=pk).order_by("nom")
            return specialites
        except:
            pass

        try:
            pk=self.request.GET["filiere"]
            pk=int(pk)
            specialites=Specialite.objects.filter(filiere__pk=pk).order_by("nom")
            return specialites
        except:
            pass

        try:
            search=self.request.GET["search"]
            specialites=Specialite.objects.filter(nom__icontains=search).order_by("nom")
            return specialites
        except:
            pass

        return Specialite.objects.all().order_by("nom")







@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def editionEmploiDeTemps(request, pk):

    context={}
    specialite=get_object_or_404(Specialite, pk=pk)
    request.session["pk_specialite"]=pk

    try:
        emploiDeTemps=Emploi.objects.get(specialite__pk=pk)
    except Emploi.DoesNotExist:
        emploiDeTemps=Emploi(semestre=1)
        emploi_de_temps_journaliers=[]
        for _ in range(6):
            emploi_de_temps_journaliers.append(EmploiDeTempsJounalier.objects.create())


        emploiDeTemps.lundi=emploi_de_temps_journaliers[0]
        emploiDeTemps.mardi=emploi_de_temps_journaliers[1]
        emploiDeTemps.mercredi=emploi_de_temps_journaliers[2]
        emploiDeTemps.jeudi=emploi_de_temps_journaliers[3]
        emploiDeTemps.vendredi=emploi_de_temps_journaliers[4]
        emploiDeTemps.samedi=emploi_de_temps_journaliers[5]
        emploiDeTemps.save()


        specialite.emploi_de_temps=emploiDeTemps
        specialite.save()





    form=EmploiDeTempsForm()
    error_=None

    if (request.method=="POST" and request.is_ajax()):
        form=EmploiDeTempsForm(request.POST)
        if form.is_valid():

            fields_={"lundi":[form.cleaned_data["field_11"],
                            form.cleaned_data["field_12"],
                            form.cleaned_data["field_13"],
                            form.cleaned_data["field_14"],
                            form.cleaned_data["field_15"],
                            form.cleaned_data["field_16"],
                            form.cleaned_data["field_17"],
                            form.cleaned_data["field_18"],
                            form.cleaned_data["field_19"],
                            ],
                    "mardi":[
                            form.cleaned_data["field_21"],
                            form.cleaned_data["field_22"],
                            form.cleaned_data["field_23"],
                            form.cleaned_data["field_24"],
                            form.cleaned_data["field_25"],
                            form.cleaned_data["field_26"],
                            form.cleaned_data["field_27"],
                            form.cleaned_data["field_28"],
                            form.cleaned_data["field_29"],
                            ],
                    "mercredi":[
                            form.cleaned_data["field_31"],
                            form.cleaned_data["field_32"],
                            form.cleaned_data["field_33"],
                            form.cleaned_data["field_34"],
                            form.cleaned_data["field_35"],
                            form.cleaned_data["field_36"],
                            form.cleaned_data["field_37"],
                            form.cleaned_data["field_38"],
                            form.cleaned_data["field_39"],
                            ],
                    "jeudi":[
                            form.cleaned_data["field_41"],
                            form.cleaned_data["field_42"],
                            form.cleaned_data["field_43"],
                            form.cleaned_data["field_44"],
                            form.cleaned_data["field_45"],
                            form.cleaned_data["field_46"],
                            form.cleaned_data["field_47"],
                            form.cleaned_data["field_48"],
                            form.cleaned_data["field_49"],
                            ],
                    "vendredi":[
                            form.cleaned_data["field_51"],
                            form.cleaned_data["field_52"],
                            form.cleaned_data["field_53"],
                            form.cleaned_data["field_54"],
                            form.cleaned_data["field_55"],
                            form.cleaned_data["field_56"],
                            form.cleaned_data["field_57"],
                            form.cleaned_data["field_58"],
                            form.cleaned_data["field_59"],
                            ],
                    "samedi":[
                            form.cleaned_data["field_61"],
                            form.cleaned_data["field_62"],
                            form.cleaned_data["field_63"],
                            form.cleaned_data["field_64"],
                            form.cleaned_data["field_65"],
                            form.cleaned_data["field_66"],
                            form.cleaned_data["field_67"],
                            form.cleaned_data["field_68"],
                            form.cleaned_data["field_69"],
                            ],}


            for nom_jour, fields in fields_.items():
                matieres=[]
                periode=0
                for field in fields:
                    periode+=1
                    if field=="":
                        matieres.append(None)
                    else:
                        field=field.split("-")
                        pk_matiere=field[0]

                        try:
                            pk_professeur=field[1]
                            pk_professeur=int(pk_professeur)
                        except:
                            pass
                            pk_professeur=None
                        try:
                            pk_matiere=int(pk_matiere)
                            matiere=Matiere.objects.get(pk=pk_matiere)

                            if pk_professeur is not None:

                                professeur=Professeur.objects.get(pk=pk_professeur)
                        except:
                            pk_matiere=""
                            matiere=None

                            #context["error_"]="Erreur lors de l'enregistrement"

                            #return render(request, "direction/edition-emploi-de-temps.html", context)
                        if matiere is not None:
                            if pk_professeur is not None:

                                definitionEmploiDeTempsProfesseur(professeur, nom_jour, periode, matiere )
                                matiere.professeur=professeur

                            else:
                                matiere.professeur=None

                            matiere.save()
                        matieres.append(matiere)



                if nom_jour=="lundi":
                    jour=emploiDeTemps.lundi


                elif nom_jour=="mardi":
                    jour=emploiDeTemps.mardi
                elif nom_jour=="mercredi":
                    jour=emploiDeTemps.mercredi
                elif nom_jour=="jeudi":
                    jour=emploiDeTemps.jeudi
                elif nom_jour=="vendredi":
                    jour=emploiDeTemps.vendredi
                elif nom_jour=="samedi":
                    jour=emploiDeTemps.samedi

                jour.periode1=matieres[0]
                jour.periode2=matieres[1]
                jour.periode3=matieres[2]
                jour.periode4=matieres[3]
                jour.periode5=matieres[4]
                jour.periode6=matieres[5]
                jour.periode7=matieres[6]
                jour.periode8=matieres[7]
                jour.periode9=matieres[8]

                jour.save()


                specialite.save()





            return JsonResponse({"error": True})


    jours=[emploiDeTemps.lundi, emploiDeTemps.mardi, emploiDeTemps.mercredi,
            emploiDeTemps.jeudi, emploiDeTemps.vendredi, emploiDeTemps.samedi]

    periode1={"periode":1, "heure":datetime.time(7, 30)}
    index=1
    for jour in jours:
        key="jour_%s"%index

        try:
            pk_matiere=jour.periode1.pk

        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode1.professeur.pk
        except:
            pk_professeur=""
        periode1[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1

    periode2={"periode":2, "heure":datetime.time(8, 30)}


    index=1
    for jour in jours:
        key="jour_%s"%index
        try:

            pk_matiere=jour.periode2.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode2.professeur.pk
        except:
            pk_professeur=""
        periode2[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1


    index=1
    periode3={"periode":3, "heure":datetime.time(9, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode3.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode3.professeur.pk
        except:
            pk_professeur=""
        periode3[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1


    index=1
    periode4={"periode":4, "heure":datetime.time(10, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode4.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode4.professeur.pk
        except:
            pk_professeur=""
        periode4[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1


    index=1
    periode5={"periode":5, "heure":datetime.time(11, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode5.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode5.professeur.pk
        except:
            pk_professeur=""
        periode5[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1


    index=1
    periode6={"periode":6, "heure":datetime.time(12, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode6.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode6.matiere.pk
        except:
            pk_professeur=""
        periode6[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1

    index=1
    periode7={"periode":7, "heure":datetime.time(13, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode7.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode7.professeur.pk
        except:
            pk_professeur=""
        periode7[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1

    index=1
    periode8={"periode":8, "heure":datetime.time(14, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode8.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode8.professeur.pk
        except:
            pk_professeur=""
        periode8[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1

    index=1
    periode9={"periode":9, "heure":datetime.time(15, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            pk_matiere=jour.periode9.pk
        except:
            pk_matiere=""
        try:
            pk_professeur=jour.periode9.professeur.pk
        except:
            pk_professeur=""
        periode9[key]="{}-{}".format(pk_matiere, pk_professeur)
        index+=1
    tableau_emploi_de_temps=[periode1, periode2, periode3, periode4, periode5,
    periode6, periode7, periode8, periode9]

    context["tableau_emploi_de_temps"]=tableau_emploi_de_temps
    context["form"]=form
    context["error_"]=error_
    context["specialite"]=specialite
    domaines=DomaineEtude.objects.all()
    context["domaines"]=domaines
    context["professeurs"]=Professeur.objects.all()


    matieres=specialite.matiere_set.all()
    context["matieres"]=matieres
    return render(request, "direction/edition-emploi-de-temps.html", context)

def definitionEmploiDeTempsProfesseur(professeur, jour, periode, matiere):
    if professeur.emploi_de_temps is None:
        professeur.emploi_de_temps=Emploi.objects.create()
        professeur.save()
    emploi_de_temps=professeur.emploi_de_temps
    if jour=="lundi":
        jour=emploi_de_temps.lundi


        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            print(jour)
            emploi_de_temps.lundi=jour
    elif jour=="mardi":
        jour=emploi_de_temps.mardi
        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            emploi_de_temps.mardi=jour
    elif jour=="mercredi":
        jour=emploi_de_temps.mercredi
        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            emploi_de_temps.mercredi=jour
    elif jour=="jeudi":
        jour=emploi_de_temps.jeudi
        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            emploi_de_temps.jeudi=jour
    elif jour=="vendredi":
        jour=emploi_de_temps.vendredi
        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            emploi_de_temps.vendredi=jour
    elif jour=="samedi":
        jour=emploi_de_temps.samedi
        if jour is None:
            jour=EmploiDeTempsJounalier.objects.create()
            emploi_de_temps.samedi=jour


    emploi_de_temps.save()


    if periode==1:
        jour.periode1=matiere
    elif periode==2:
        jour.periode2=matiere
    elif periode==3:
        jour.periode3=matiere
    elif periode==4:
        jour.periode4=matiere
    elif periode==5:
        jour.periode5=matiere
    elif periode==6:
        jour.periode6=matiere
    elif periode==7:
        jour.periode7=matiere
    elif periode==8:
        jour.periode8=matiere
    elif periode==9:
        jour.periode9=matiere



    jour.save()






@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def emploiDeTempsModificationProfesseur(request, pk):
    try:
        search=request.GET["search"]
    except:
        search="tout"
    try:
        pk=int(pk)
        if pk!=0:
            matiere=Matiere.objects.get(pk=pk)
            domaines=matiere.domaine.all()
            professeurs=Professeur.objects.filter(domaine__in=domaines)
            if search!="tout":
                professeurs=professeurs.filter(Q(noms__icontains=search) | Q(prenoms__icontains=search))
            domaines=list(domaines.values())
            professeurs=list(professeurs.values("pk", "noms", "prenoms"))
            response={"domaines":domaines, "pk_matiere":matiere.pk,
            "nom_matiere":matiere.nom, "professeurs":professeurs}
        else:
            professeurs=Professeur.objects.all()
            if search!="tout":
                professeurs=professeurs.filter(Q(noms__icontains=search) | Q(prenoms__icontains=search))
            print(professeurs)
            professeurs=list(professeurs.values("pk", "noms", "prenoms"))

            response={"professeurs":professeurs}
    except:
        response={"error": "Erreur lors de la recherche"}

    return JsonResponse(response)



@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def  emploiDeTempsDetailsProfesseur(request, pk):
    pk=int(pk)
    professeur=Professeur.objects.filter(pk=pk)
    if len(professeur)!=1:
        raise TypeError #§§§§§§§§§§TML

    cv=professeur[0].cv
    domaines=professeur[0].domaine.all()
    professeur=professeur.values("photo", "matricule", "noms", "prenoms", "date_naissance",
    "lieu_de_naissance", "email", "numero_telephone", "nationalite", "numero_CNI")
    professeur=list(professeur)
    cv={"nom_diplomes":cv.nom_diplomes, "annee_obtension_diplome":cv.annee_obtension_diplome,
     "ecole_obtension_diplome": cv.ecole_obtension_diplome}
    domaines=domaines.values("nom")
    domaines=list(domaines)
    response={"professeur":professeur, "cv":cv, "domaines":domaines}

    return JsonResponse(response)


@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def emploiDeTempsDetailsMatiere(request, pk):
    pk=int(pk)
    matiere=Matiere.objects.filter(pk=pk)
    if len(matiere)!=1:
        raise TypeError  #§§§§§§§§§§TML
    domaines=matiere[0].domaine.all()
    specialite=matiere[0].specialite
    matiere=matiere.values("nom", "programme", "credit", "semestre")
    matiere=list(matiere)
    specialite={"nom": specialite.nom, "nom_filiere": specialite.filiere.nom,
    "nom_cycle": specialite.filiere.cycle.nom}
    domaines=domaines.values("nom")
    domaines=list(domaines)
    response={"matiere": matiere, "specialite":specialite, "domaines": domaines}


    return JsonResponse(response)

@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def selectionProfesseur(request):
    try:
        pk_specialite=request.session["pk_specialite"]
        parametre=request.GET["p"]
        pk_professeur=request.GET["prof"]
        pk_professeur=int(pk_professeur)
        professeur=Professeur.objects.get(pk=pk_professeur)
        parametre=parametre.split("/")
        print(parametre)
        #parametre.sort()
        response={"1":[],"2":[],"3":[],"4":[],"5":[],"6":[], }
        for p in parametre:
            jour_=p[0]
            periode=p[1]

            if jour_=="1":
                jour=professeur.emploi_de_temps.lundi
            elif jour_=="2":
                jour=professeur.emploi_de_temps.mardi
            elif jour_=="3":
                jour=professeur.emploi_de_temps.mercredi
            elif jour_=="4":
                jour=professeur.emploi_de_temps.jeudi
            elif jour_=="5":
                jour=professeur.emploi_de_temps.vendredi
            elif jour_=="6":
                jour=professeur.emploi_de_temps.samedi
            else:
                raise TypeError



            if periode=="1":
                try:
                    matiere=jour.periode1.pk
                    if jour.periode1.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)
                except AttributeError:
                    pass

            elif periode=="2":
                try:
                    matiere=jour.periode2.pk
                    if jour.periode2.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass


            elif periode=="3":
                try:
                    matiere=jour.periode3.pk
                    if jour.periode3.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)
                except AttributeError:
                    pass

            elif periode=="4":
                try:
                    matiere=jour.periode4.pk
                    if jour.periode4.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass

            elif periode=="5":
                try:
                    matiere=jour.periode5.pk
                    if jour.periode5.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass

            elif periode=="6":
                try:
                    matiere=jour.periode6.pk
                    if jour.periode6.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass

            elif periode=="7":
                try:
                    matiere=jour.periode7.pk
                    if jour.periode7.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass

            elif periode=="8":
                try:
                    matiere=jour.periode8.pk
                    if jour.periode8.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass

            elif periode=="9":
                try:
                    matiere=jour.periode9.pk
                    if jour.periode9.specialite.pk!=pk_specialite:
                        response[jour_].append(periode)

                except AttributeError:
                    pass
            else:
                raise TypeError

    except:
        response={"error": True}

    return JsonResponse(response)


@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def selectionProfesseur1(request):
    error=False
    parametre=request.GET["p"]
    pk_professeur=request.GET["prof"]
    pk_professeur=int(pk_professeur)
    professeur=Professeur.objects.get(pk=pk_professeur)
    jour_=parametre[0]
    periode=parametre[1]
    if jour_=="1":
        jour=professeur.emploi_de_temps.lundi
    elif jour_=="2":
        jour=professeur.emploi_de_temps.mardi
    elif jour_=="3":
        jour=professeur.emploi_de_temps.mercredi
    elif jour_=="4":
        jour=professeur.emploi_de_temps.jeudi
    elif jour_=="5":
        jour=professeur.emploi_de_temps.vendredi
    elif jour_=="6":
        jour=professeur.emploi_de_temps.samedi
    else:
        raise TypeError


    if periode=="1":
        try:
            matiere=jour.periode1.pk
            error=True
        except AttributeError:
            pass
    elif periode=="2":
        try:
            matiere=jour.periode2.pk
            error=True
        except AttributeError:
            pass
    elif periode=="3":
        try:
            matiere=jour.periode3.pk
            error=True
        except AttributeError:
            pass
    elif periode=="4":
        try:
            matiere=jour.periode4.pk
            error=True
        except AttributeError:
            pass
    elif periode=="5":
        try:
            matiere=jour.periode5.pk
            error=True
        except AttributeError:
            pass
    elif periode=="6":
        try:
            matiere=jour.periode6.pk
            error=True
        except AttributeError:
            pass
    elif periode=="7":
        try:
            matiere=jour.periode7.pk
            error=True
        except AttributeError:
            pass
    elif periode=="8":
        try:
            matiere=jour.periode8.pk
            error=True
        except AttributeError:
            pass
    elif periode=="9":
        try:
            matiere=jour.periode9.pk
            error=True
        except AttributeError:
            pass
    else:
        raise TypeError

    return JsonResponse({"error":error})

@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def affichageEmploiDeTempsProfesseur(request, pk):

    professeur=get_object_or_404(Professeur, pk=pk)
    emploiDeTemps=professeur.emploi_de_temps
    jours=[emploiDeTemps.lundi, emploiDeTemps.mardi, emploiDeTemps.mercredi,
            emploiDeTemps.jeudi, emploiDeTemps.vendredi, emploiDeTemps.samedi]

    periode1={"periode":1, "heure":datetime.time(7, 30)}
    index=1
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode1.nom
            credit=jour.periode1.credit
            specialite=jour.periode1.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode1[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1

    periode2={"periode":2, "heure":datetime.time(8, 30)}


    index=1
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode2.nom
            credit=jour.periode2.credit
            specialite=jour.periode2.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode2[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1


    index=1
    periode3={"periode":3, "heure":datetime.time(9, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode3.nom
            credit=jour.periode3.credit
            specialite=jour.periode3.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode3[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1


    index=1
    periode4={"periode":4, "heure":datetime.time(10, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode4.nom
            credit=jour.periode4.credit
            specialite=jour.periode4.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode4[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1


    index=1
    periode5={"periode":5, "heure":datetime.time(11, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode5.nom
            credit=jour.periode5.credit
            specialite=jour.periode5.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode5[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1


    index=1
    periode6={"periode":6, "heure":datetime.time(12, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode6.nom
            credit=jour.periode6.credit
            specialite=jour.periode6.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode6[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1

    index=1
    periode7={"periode":7, "heure":datetime.time(13, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode7.nom
            credit=jour.periode7.credit
            specialite=jour.periode7.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode7[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1

    index=1
    periode8={"periode":8, "heure":datetime.time(14, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode8.nom
            credit=jour.periode8.credit
            specialite=jour.periode8.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode8[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1

    index=1
    periode9={"periode":9, "heure":datetime.time(15, 30)}
    for jour in jours:
        key="jour_%s"%index
        try:
            nom_matiere=jour.periode9.nom
            credit=jour.periode9.credit
            specialite=jour.periode9.specialite
        except:
            specialite=""
            nom_matiere=""
            credit=None
        periode9[key]={"nom_matiere":nom_matiere, "credit":credit, "specialite":specialite}
        index+=1
    tableau_emploi_de_temps=[periode1, periode2, periode3, periode4, periode5,
    periode6, periode7, periode8, periode9]
    context={}
    context["professeur"]=professeur
    context["emploi_de_temps"]=tableau_emploi_de_temps

    return render(request, "direction/affichage_emploi_de_temps_professeur.html", context )


@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def cours(request):
    return render(request, "direction/cours.html", {})

class ListeCours(UserPassesTestMixin, ListView):
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="professeur")
            return True
        except:
            return False
    template_name="direction/liste-cours.html"
    context_object_name="cours"
    model=Cours

    def get_context_data(self, **kwargs):
        try:
            pk_professeur=self.request.session["pk_professeur"]
        except:
            raise Http404
        professeur=get_object_or_404(Professeur, pk=pk_professeur)
        specialites=[]
        for matiere in professeur.matiere_set.all():
            specialites.append(matiere.specialite)
        context=super().get_context_data(**kwargs)
        context["specialites"]=specialites
        context["length_cours"]=len(context["cours"])
        try:
            pk_specialite=self.request.GET["specialite"]
            pk_specialite=int(pk_specialite)
            if pk_specialite not in [specialite.pk for specialite in context["specialites"]]:
                raise TypeError
            context["specialite_active"]=pk_specialite
        except:
            pass

        return context

    def get_queryset(self):
        try:
            pk_specialite=self.request.GET["specialite"]
            pk_specialite=int(pk_specialite)
        except:
            pk_specialite=0

        cours=[]
        try:
            pk_professeur=self.request.session["pk_professeur"]
        except:
            raise Http404
        professeur=get_object_or_404(Professeur, pk=pk_professeur)
        matieres=professeur.matiere_set.filter(specialite__pk=pk_specialite)
        if len(matieres)==0:
            matieres=professeur.matiere_set.all()
        for matiere in matieres :
            for cours_ in matiere.specialite.cours.all():
                cours.append(cours_)


        return cours
@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def selectionSpecialite(request):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    context={}
    try:
        prev=request.GET["prev"]
        if prev=="0":
            prev="/direction/cours/"
        else:
            prev="/direction/cours/liste_cours/"
    except:
        prev="/direction/cours/liste_cours/"
    context["prev"]=prev
    specialites=[]
    for matiere in professeur.matiere_set.all():
        specialites.append(matiere.specialite)
    context["specialites"]=specialites
    return render(request, "direction/selection-specialite.html", context)


class AjoutCours(UserPassesTestMixin ,CreateView):
    template_name="direction/ajout-cours.html"
    form_class=AjoutCoursForm
    model=Cours
    success_url="/direction/cours/liste_cours/"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        try:
            prev=self.request.GET["prev"]
        except:
            prev="/direction/cours/selection_specialite/?prev=0"
        context["prev"]=prev

        return context

    def post(self, request, *args, **kwargs ):
        specialite=get_object_or_404(Specialite, pk=kwargs["pk_specialite"])
        form=AjoutCoursForm(request.POST, request.FILES)
        if form.is_valid():
            cours=form.save()
            specialite.cours.add(cours)
            specialite.save()
            return redirect(self.success_url)
        return render(request, "direction/ajout-cours.html", {"form":form})

class LireCours(UserPassesTestMixin,  DetailView):
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="professeur")
            return True
        except:
            return False
    template_name="direction/lire-cours.html"
    context_object_name="cours"
    model=Cours




class ModificationCours(UserPassesTestMixin, UpdateView):
    def test_func(self):
        try:
            group=self.request.user.groups.get(name="professeur")
            return True
        except:
            return False

    template_name="direction/modification-cours.html"
    context_object_name="cours"
    form_class=AjoutCoursForm
    model=Cours
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cours=context["cours"]
        context["prev"]=reverse("direction:lire_cours", kwargs={"pk": cours.pk})
        return context

class SuppressionCours(UserPassesTestMixin, DeleteView):

    def test_func(self):
        try:
            group=self.request.user.groups.get(name="professeur")
            return True
        except:
            return False
    template_name="direction/suppression-cours.html"
    context_object_name="cours"
    model=Cours
    success_url="/direction/cours/liste_cours/"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cours=context["cours"]
        context["prev"]=reverse("direction:lire_cours", kwargs={"pk": cours.pk})
        return context


@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def selectionSpecialitePourNote(request):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    context={}
    specialites=[]
    for matiere in professeur.matiere_set.all():
        specialites.append(matiere.specialite)
    context["specialites"]=specialites
    return render(request, "direction/selection-specialite-pour-note.html", context)


@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def editionNotes(request, pk):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    specialite=get_object_or_404(Specialite, pk=pk)
    context={}
    context["error"]=""
    context["id_error"]=[]
    if request.method=="POST":

        try:

            data=dict(request.POST)

            data.pop("csrfmiddlewaretoken")

            for key, value in data.items():
                try:
                    value=(value[0])
                    value=value.split(",")
                    value=".".join(value)
                    value=float(value)
                except ValueError:
                    pass
                else:
                    if (value<0.00 or value>20.00):
                        context["error"]="les notes doivent êtres comprisent entre 0 et 20"
                        context["id_error"].append(key)
                    else:
                        key=key.split("-")
                        examen=key[0]
                        pk_matiere=key[1]
                        pk_matiere=int(pk_matiere)
                        pk_etudiant=key[2]
                        pk_etudiant=int(pk_etudiant)
                        matiere=Matiere.objects.get(pk=pk_matiere)
                        etudiant=Etudiant.objects.get(pk=pk_etudiant)
                        notes=Note.objects.filter(Q(matiere__pk=pk_matiere) & Q(etudiant__pk=pk_etudiant))
                        if len(notes)!=0:
                            note=notes[0]
                        else:
                            note=Note(matiere=matiere, etudiant=etudiant)

                        if examen=="cc1":
                            note.cc1=value
                        elif examen=="sn1":
                            note.sn1=value
                        elif examen=="cc2":
                            note.cc2=value
                        elif examen=="sn2":
                            note.sn2=value
                        note.save()
        except:
            context["error"]=1
    else:
        context["error"]=""
    context["specialite"]=specialite
    matieres=[]
    for matiere in specialite.matiere_set.filter(professeur__pk=pk_professeur):
        matieres.append(matiere)
    context["matieres"]=matieres
    etudiants=specialite.etudiant_set.all()
    context["etudiants"]=etudiants
    prev="/direction/notes/selection_specialite_pour_note/"
    context["prev"]=prev

    return render(request, "direction/edition-notes.html", context)

@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def delegue(request):
    context={}
    context["filtre_cycle"]=Cycle.objects.all()
    context["filtre_filiere"]=Filiere.objects.all()
    try:
        pk_cycle=request.GET["cycle"]
        pk_cycle=int(pk_cycle)
        cycle=Cycle.objects.get(pk=pk_cycle)
        specialites=Specialite.objects.filter(filiere__cycle__pk=pk_cycle)
        context["active_cycle"]=pk_cycle
    except:
        try:
            pk_filiere=request.GET["filiere"]
            pk_filiere=int(pk_filiere)
            filiere=Filiere.objects.get(pk=pk_filiere)
            specialites=Specialite.objects.filter(filiere__pk=pk_filiere)
            context["active_filiere"]=pk_filiere
        except:
            try:
                search=request.GET["search"]
                specialites=Specialite.objects.filter(nom__icontains=search)
            except:
                specialites=Specialite.objects.all()


    context["specialites"]=specialites


    return render(request, "direction/delegue.html", context)


@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def editionDelegue(request, pk_specialite):
    pk_specialite=int(pk_specialite)
    specialite=get_object_or_404(Specialite, pk=pk_specialite)
    context={}
    context["specialite"]=specialite
    context["prev"]=reverse("direction:delegue")
    try:
        search=request.GET["search"]
        searchBy=request.GET["search-by"]
        if searchBy=="matricule":
            search=int(search)
            etudiants=Etudiant.objects.filter(Q(specialite__pk=pk_specialite)&Q(matricule=search))
        elif searchBy=="noms":
            etudiants=Etudiant.objects.filter(specialite__pk=pk_specialite).filter(Q(noms__icontains=search)|Q(prenoms__icontains=search))
        else:
            raise TypeError
    except:
        etudiants=Etudiant.objects.filter(specialite__pk=pk_specialite)

    context["etudiants"]=etudiants
    return render(request, "direction/edition-delegue.html", context)

@user_passes_test(test_func=testDirecteurAcademique, login_url=LOGIN_URL_PASSES_TEST)
def setDelegue(request, pk_etudiant):
    pk_etudiant=int(pk_etudiant)
    etudiant=get_object_or_404(Etudiant, pk=pk_etudiant)
    specialite=etudiant.specialite
    specialite.delegue=etudiant
    specialite.save()
    return redirect(reverse("direction:edition_delegue", args=[specialite.pk]))


@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def  absenceEtudiant(request):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    context={}
    specialites=[]
    for matiere in professeur.matiere_set.all():
        specialites.append(matiere.specialite)
    context["specialites"]=specialites

    return render(request, "direction/absence-etudiant.html", context)

@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def editionAbsenceEtudiant(request, pk_specialite):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    pk_specialite=int(pk_specialite)
    specialite=get_object_or_404(Specialite, pk=pk_specialite)
    context={}
    context["specialite"]=specialite
    context["error"]=None
    form=AbsenceEtudiantForm()
    if request.method=="POST":
        context["error"]=False
        form=AbsenceEtudiantForm(request.POST, error_class=ParagraphErrorList)
        absents=[]
        if form.is_valid():
            date=form.cleaned_data["date"]
            heure_debut=form.cleaned_data["heure_debut"]
            heure_fin=form.cleaned_data["heure_fin"]


            try:
                for etudiant in specialite.etudiant_set.all():
                    absence=AbsenceEtudiant.objects.get_or_create(date=date, heure_debut=heure_debut,
                    heure_fin=heure_fin, etudiant=etudiant, professeur=professeur)
                    absence=absence[0]
                    if request.POST[str(etudiant.pk)]=="1":
                        absence.delete()
                    elif request.POST[str(etudiant.pk)]=="0":
                        absents.append(etudiant.pk)


            except:
                context["error"]=True
        else:
            context["error"]=True
            for etudiant in specialite.etudiant_set.all():
                if request.POST[str(etudiant.pk)]=="0":
                    absents.append(etudiant.pk)


        context["absents"]=absents



    context["form"]=form
    context["prev"]="/direction/absence_etudiant/"

    return render(request, "direction/edition-absence-etudiant.html", context)



@user_passes_test(test_func=testProfesseur, login_url=LOGIN_URL_TEST_PROFESSEUR)
def listeAbsenceEtudiant(request, pk_specialite):
    try:
        pk_professeur=request.session["pk_professeur"]
    except:
        raise Http404
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    pk_specialite=int(pk_specialite)
    specialite=get_object_or_404(Specialite, pk=pk_specialite)
    context={}
    context["specialite"]=specialite

    etudiants=specialite.etudiant_set.annotate(heures=Sum(F("absence__heure_fin")-F("absence__heure_debut")))
    for etudiant in etudiants:
        heures=etudiant.heures
        secondes=heures.total_seconds()
        heures=int(secondes//3600)
        minutes=int((secondes%3600)//60)
        etudiant.heures="{}h {}min".format(heures, minutes)

    #for etudiant in specialite.etudiant_set.all():
        #etudiant=etudiant.absse.annotate(heures=Sum(F("heure_fin")-F("heure_debut")))
        #etudiants.append(etudiant)
    context["etudiants"]=etudiants


    return render(request, "direction/liste-absence-etudiant.html", context)

@user_passes_test(test_func=testDelegue, login_url=LOGIN_URL_PASSES_TEST)
def absenceProfesseur(request):
    try:
        pk_delegue=request.session["pk_delegue"]
    except:
        raise Http404
    delegue=get_object_or_404(Etudiant, pk=pk_delegue)
    matieres=delegue.specialite.matiere_set.exclude(professeur=None)
    context={}
    context["matieres"]=matieres
    return render(request, "direction/absence-professeur.html", context)

@user_passes_test(test_func=testDelegue, login_url=LOGIN_URL_PASSES_TEST)
def editionAbsenceProfesseur(request, pk_professeur):
    try:
        pk_delegue=request.session["pk_delegue"]
    except:
        raise Http404
    delegue=get_object_or_404(Etudiant, pk=pk_delegue)
    pk_professeur=int(pk_professeur)
    professeur=get_object_or_404(Professeur, pk=pk_professeur)
    context={}
    context["professeur"]=professeur
    present_=True
    error=None
    form=AbsenceProfesseurForm()
    if request.method=="POST":
        form=AbsenceProfesseurForm(request.POST, error_class=ParagraphErrorList)
        error=False
        if form.is_valid():

            try:
                presence=request.POST["presence"]
                presence=True
            except KeyError:
                presence=False
            finally:
                date=form.cleaned_data["date"]
                heure_debut=form.cleaned_data["heure_debut"]
                heure_fin=form.cleaned_data["heure_fin"]

                absence=AbsenceProfesseur.objects.get_or_create(date=date, heure_debut=heure_debut,
                heure_fin=heure_fin, professeur=professeur)
                absence=absence[0]
                if presence:
                    absence.delete()
                else:
                    present_=False

        else:
            error=True
    secondes=0
    for absence in professeur.absence.all():
        secondes+=((absence.heure_fin.hour*3600+absence.heure_fin.minute*60)-(absence.heure_debut.hour*3600+absence.heure_debut.minute*60))

    heures=int(secondes//3600)
    minutes=int((secondes%3600)//60)
    context["heures"]="{}h {}min".format(heures, minutes)

    context["present_"]=present_
    context["form"]=form
    context["error"]=error
    return render(request, "direction/edition-absence-professeur.html", context)
