from django import forms
from django.contrib.auth.forms import AuthenticationForm



class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(max_length=150, widget=forms.PasswordInput())
