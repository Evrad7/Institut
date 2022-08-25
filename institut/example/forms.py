from django import forms
from .models import Jeu


class JeuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})
    class Meta:
        model=Jeu
        exclude=[""]
