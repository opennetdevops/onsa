from django import forms
from django.core.validators import validate_slug

class ClientForm(forms.Form):
    name = forms.CharField(max_length=100)
    cuic = forms.CharField(max_length=20)
