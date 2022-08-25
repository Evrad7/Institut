from django import forms
from .models import Etudiant, Parent, Professeur, CVProfesseur, Cycle, Cours,\
AbsenceEtudiant, AbsenceProfesseur
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.utils import ErrorList


class InscriptionForm(forms.ModelForm):

    class Meta:
        model=Etudiant
        exclude=("statut", "club", "profil")



class AdminTMLDateWidget(AdminDateWidget):
    class Media:
        js = [
            'direction/js/CalendarAmin.js',
           'direction/js/DateTimeShortcutsAdmin.js',
        ]



class ParagraphErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="text-danger">%s</div>'%''.join(['<p class="">%s</p>'%e for e in self])


class AjoutParentForm(forms.ModelForm):
    #age=forms.DateField(widget=AdminDateWidget())
    error_css_class="text-danger"
    class Meta:
        model=Parent
        fields="__all__"
        widgets={
            "photo":forms.TextInput(attrs={"class":"form-control", "type":"file"}),
            "noms":forms.TextInput(attrs={"class":"form-control"}),
            "prenoms":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "date_naissance":forms.TextInput(attrs={"class":"form-control", "type":"date"}),
            "nationalite":forms.TextInput(attrs={"class":"form-control"}),
            "numero_CNI":forms.TextInput(attrs={"class":"form-control"}),
            "profession_tuteur":forms.TextInput(attrs={"class":"form-control"}),
            "numero_telephone":forms.TextInput(attrs={"class":"form-control"}),

        }

class RechercheForm(forms.Form):
    matricule=forms.IntegerField(validators=[MinValueValidator(1)], widget=forms.NumberInput(attrs={"class":"form-control"}), required=False)

    nom=forms.CharField(max_length=30,  widget=forms.TextInput(attrs={"class":"form-control "}), required=False)
    prenom=forms.CharField(max_length=30,  widget=forms.TextInput(attrs={"class":"form-control "}), required=False)



    def clean(self):
        cleaned_data=super().clean();
        if self.errors:
            return cleaned_data

        matricule=cleaned_data["matricule"]
        nom=cleaned_data["nom"]
        prenom=cleaned_data["prenom"]
        print(prenom)
        if matricule:
            return cleaned_data
        if nom :
            return cleaned_data
        raise ValidationError("entrez  aussi le nom et/ou le matricule", code="error-tml")




class AjoutEtudiantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields=[self.fields["photo"],
        self.fields["noms"],
        self.fields["prenoms"],

        self.fields["lieu_de_naissance"],
        self.fields["sexe"],
        self.fields["nationalite"],
        self.fields["numero_CNI"],
        self.fields["numero_telephone"],
        self.fields["email"],
        self.fields["ancienne_ecole"],


        ]
        for field  in fields:
            field.widget.attrs.update({"class":"form-control"})

        self.fields["cantine"].widget.attrs.update({"class":"form-check-input "})
        self.fields["transport"].widget.attrs.update({"class":"form-check-input"})
        self.fields["specialite"].widget.attrs.update({"class": "form-select bg-light"})#Look class

    error_css_class="text-danger"

    class Meta:
        model=Etudiant
        exclude=["matricule", "statut", "club", "parent", "profil", "developpment_password"]
        widgets={
        "date_de_naissance": forms.TextInput({"class":"form-control", "type":"date"})

        }




class InscriptionAncienEtudiantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.instance_=kwargs["instance"]
        except KeyError:
            pass

        self.fields_=[
        self.fields["photo"],
        self.fields["noms"],
        self.fields["prenoms"],

        self.fields["lieu_de_naissance"],
        self.fields["sexe"],
        self.fields["nationalite"],
        self.fields["numero_CNI"],
        self.fields["numero_telephone"],
        self.fields["email"],
        self.fields["ancienne_ecole"],


        ]
        for field  in self.fields_:
            field.widget.attrs.update({"class":"form-control", "readonly":"true"})

        self.fields["cantine"].widget.attrs.update({"class":"form-check-input "})
        self.fields["transport"].widget.attrs.update({"class":"form-check-input"})
        self.fields["specialite"].widget.attrs.update({"class": "form-select bg-light"})#Look class

    error_css_class="text-danger"

    class Meta:
        model=Etudiant
        exclude=["matricule", "statut", "club", "parent", "profil", "developpment_password"]
        widgets={
        "date_de_naissance": forms.TextInput({"class":"form-control", "type":"date", "readonly":"true"})

        }


class ModificationEtudiantForm(forms.ModelForm):

    class Meta:
        exclude=["matricule", "statut", "club", ""]


class AjoutProfesseurForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields_=[
            self.fields["photo"],
            self.fields["noms"],
            self.fields["prenoms"],
            self.fields["lieu_de_naissance"],
            self.fields["email"],
            self.fields["numero_telephone"],
            self.fields["domaine"],
            self.fields["nationalite"],
            self.fields["numero_CNI"],
        ]

        for field in self.fields_:
            field.widget.attrs.update({"class":"form-control"})

    class Meta:
        model=Professeur
        exclude=["cv", "emploi_de_temps", "profil", "developpment_password", "matricule"]
        widgets={
        "date_naissance":forms.TextInput(attrs={"class":"form-control", "type":"date"})
        }


class AjoutCVForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})


    class Meta:
        model=CVProfesseur
        fields=["nom_diplomes", "annee_obtension_diplome", "ecole_obtension_diplome"]
        labels={
        "nom_diplomes":"nom du diplome",
        "annee_obtension_diplome":"année d'obtention du diplome",
        "ecole_obtension_diplome":"ecole d'obtention du diplome",

        }


class EmploiDeTempsForm(forms.Form):

    field_11=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_12=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_13=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_14=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_15=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_16=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_17=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_18=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_19=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

    field_21=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_22=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_23=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_24=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_25=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_26=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_27=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_28=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_29=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

    field_31=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_32=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_33=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_34=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_35=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_36=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_37=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_38=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_39=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

    field_41=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_42=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_43=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_44=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_45=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_46=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_47=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_48=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_49=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

    field_51=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_52=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_53=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_54=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_55=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_56=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_57=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_58=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_59=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

    field_61=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_62=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_63=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_64=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_65=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_66=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_67=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_68=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)
    field_69=forms.CharField(max_length=30, widget=forms.HiddenInput(), required=False)

class AjoutCoursForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model=Cours
        exclude=[""]

class AbsenceEtudiantForm(forms.ModelForm):
    error_css_class="text-danger"

    class Meta:
        model=AbsenceEtudiant
        exclude=["professeur", "etudiant", "motif"]
        widgets={
        "date":forms.TextInput(attrs={"class":"form-control", "type":"date", "required":"True"}),
        "heure_debut":forms.TextInput(attrs={"class":"form-control", "type":"time", "required":"True"}),
        "heure_fin":forms.TextInput(attrs={"class":"form-control", "type":"time", "required":"True"}),
        }
class AbsenceProfesseurForm(forms.ModelForm):
    error_css_class="text-danger"
    class Meta:
        model=AbsenceProfesseur
        exclude=["professeur", "motif"]
        widgets={
        "date":forms.TextInput(attrs={"class":"form-control", "type":"date", "required":"True"}),
        "heure_debut":forms.TextInput(attrs={"class":"form-control", "type":"time", "required":"True"}),
        "heure_fin":forms.TextInput(attrs={"class":"form-control", "type":"time", "required":"True"}),
        }
