from django.urls import path

from .views import index, etudiant, professeur, parametre,\
 quitter, parent, inscription, rechercheAncienEtudiant, ajoutParent,\
ajoutEtudiant, ModificationEtudiant, inscriptionAcienEtudiant, ListeEtudiant,\
LireEtudiant, SuppressionEtudiant, insertionParent, echangeParent,\
ListeParent, ModificationParent, suppressionParent, rechercheParent,LireParent,\
professeur, ajoutProfesseur, ajoutCV, ListeProfesseur, LireProfesseur,\
ModificationProfesseur, SuppressionProfesseur, rechercheProfesseur,\
ModificationCV, LireCV, EmploiDeTemps, editionEmploiDeTemps, emploiDeTempsModificationProfesseur,\
  emploiDeTempsDetailsProfesseur,  emploiDeTempsDetailsMatiere, selectionProfesseur,\
  selectionProfesseur1, affichageEmploiDeTempsProfesseur, cours, ListeCours, AjoutCours,\
  ModificationCours, SuppressionCours, selectionSpecialite, LireCours, selectionSpecialitePourNote,\
  editionNotes, delegue, editionDelegue, setDelegue, absenceEtudiant, absenceProfesseur,\
  editionAbsenceEtudiant, listeAbsenceEtudiant, editionAbsenceProfesseur

urlpatterns=[


    path("", index, name="acceuil"),
    path("etudiant/", etudiant, name="etudiant"),
    path("professeur/", professeur, name="professeur"),
    path("parent/", parent, name="parent"),
    path("parametre/", parametre, name="parametre"),

    path("quitter/", quitter, name="quitter"),
    path("etudiant/inscription/<old>/", inscription, name="inscription"),
    path("etudiant/recherche_ancien_etudiant/<int:next_>/", rechercheAncienEtudiant, name="recherche_ancien_etudiant"),
    path("parent/ajout_parent/", ajoutParent, name="ajout_parent"),
    path("etudiant/ajout_etudiant/", ajoutEtudiant, name="ajout_etudiant"),
    path("etudiant/modification_etudiant/<int:pk>/", ModificationEtudiant.as_view(), name="modification_etudiant"),
    path("etudiant/inscription_ancien_etudiant/<int:matricule>", inscriptionAcienEtudiant, name="inscription_ancien_etudiant"),
    path("etudiant/liste_etudiant/", ListeEtudiant.as_view(), name="liste_etudiant"),
    path("etudiant/lire_etudiant/<int:pk>/", LireEtudiant.as_view(), name="lire_etudiant"),
    path("etudiant/suppression_etudiant/<int:pk>/", SuppressionEtudiant.as_view(), name="suppression_etudiant"),
    path("parent/insertion_parent/<int:choice>/", insertionParent, name="insertion_parent"),
    path("parent/echange_parent/<int:matricule>/", echangeParent, name="echange_parent"),
    path("parent/liste_parent/", ListeParent.as_view(), name="liste_parent"),
    path("parent/modification_parent/<int:pk>/", ModificationParent.as_view(), name="modification_parent"),
    path("parent/suppression_parent/", suppressionParent, name="suppression_parent"),
    path("parent/recherche_parent/", rechercheParent, name="recherche_parent"),
    path("parent/lire_parent/<int:pk>/", LireParent.as_view(), name="lire_parent"),
    path("professeur/", professeur, name="professeur"),
    path("professeur/ajout_professeur/", ajoutProfesseur, name="ajout_professeur"),
    path("professeur/ajout_cv/<int:pk>/", ajoutCV, name="ajout_cv"),
    path("professeur/liste_professeur/", ListeProfesseur.as_view(), name="liste_professeur"),
    path("professeur/lire_professeur/<int:pk>/", LireProfesseur.as_view(), name="lire_professeur"),
    path("professeur/modification_professeur/<int:pk>/",ModificationProfesseur.as_view(), name="modification_professeur" ),
    path("professeur/suppression_professeur/<int:pk>/", SuppressionProfesseur.as_view(), name="suppression_professeur"),
    path("professeur/recherche_professeur/<int:next_>/", rechercheProfesseur, name="recherche_professeur"),
    path("professeur/modification_cv/<int:pk>/", ModificationCV.as_view(), name="modification_cv"),
    path("professeur/lire_cv/<int:pk>/", LireCV.as_view(), name="lire_cv"),
    path("emploi_de_temps/", EmploiDeTemps.as_view(), name="emploi_de_temps"),
    path("emploi_de_temps/edition/<int:pk>/", editionEmploiDeTemps, name="edition_emploi_de_temps" ),
    path("emploi_de_temps/edition/modification_professeur/<int:pk>/", emploiDeTempsModificationProfesseur, name="emploi_de_temps_modification_professeur"),
    path("emploi_de_temps/edition/details_professeur/<int:pk>/", emploiDeTempsDetailsProfesseur, name="emploi_de_temps_details_professeur"),
    path("emploi_de_temps/edition/details_matiere/<int:pk>/", emploiDeTempsDetailsMatiere, name="emploi_de_temps_details_matiere"),
    path("emploi_de_temps/edition/selection_professeur/", selectionProfesseur, name="selection_professeur"),
    path("emploi_de_temps/edition/selection_professeur1/", selectionProfesseur1, name="selection_professeur_1"),
    path("emploi_de_temps/affichage/<int:pk>/", affichageEmploiDeTempsProfesseur, name="affichage_emploi_de_temps"),
    path("cours/", cours, name="cours"),
    path("cours/liste_cours/", ListeCours.as_view(), name="liste_cours"),
    path("cours/selection_specialite/", selectionSpecialite, name="selection_specialite"),
    path("cours/ajout_cours/<int:pk_specialite>/", AjoutCours.as_view(), name="ajout_cours"),
    path("cours/modification_cours/<int:pk>/", ModificationCours.as_view(), name="modification_cours"),
    path("cours/suppressionCours/<int:pk>/", SuppressionCours.as_view(), name="suppression_cours"),
    path("cours/lire_cours/<int:pk>/", LireCours.as_view(), name="lire_cours"),
    path("notes/selection_specialite/", selectionSpecialitePourNote, name="selection_specialite_pour_note" ),
    path("notes/edition/<int:pk>/", editionNotes, name="edition_notes"),
    path("delegue/", delegue, name="delegue"),
    path("delegue/edition/<int:pk_specialite>/", editionDelegue, name="edition_delegue"),
    path("delegue/edition/set/<int:pk_etudiant>/", setDelegue, name="set_delegue"),
    path("absence_etudiant/", absenceEtudiant, name="absence_etudiant"),
    path("absence_etudiant/liste/<int:pk_specialite>/", listeAbsenceEtudiant, name="liste_absence_etudiant"),
    path("absence_etudiant/edition/<int:pk_specialite>/", editionAbsenceEtudiant, name="edition_absence_etudiant"),
    path("absence_professeur/", absenceProfesseur, name="absence_professeur"),
    path("absence_professeur/edition/<int:pk_professeur>/", editionAbsenceProfesseur, name="edition_absence_professeur"),



]
