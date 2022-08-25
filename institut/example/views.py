from django.shortcuts import render
from .forms import JeuForm
from .models import Jeu
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


def page(request):
    form=JeuForm()
    if request.method=="POST":
        form=JeuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("direction:acceuil"))
    jeux=Jeu.objects.all()
    return render(request, "example/page.html", locals())
