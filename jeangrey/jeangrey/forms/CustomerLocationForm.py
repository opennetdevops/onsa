from django import forms
from django.core.validators import validate_slug, DecimalValidator

class CustomerLocationForm(forms.Form):
    client_id = forms.DecimalField(validators=[DecimalValidator(4096,0)])
    address = forms.CharField(max_length=100, validators=[validate_slug])
    description = forms.CharField(max_length=100, validators=[validate_slug])
    