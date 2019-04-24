from django import forms
from django.core.validators import DecimalValidator

class CustomerLocationForm(forms.Form):
    client_id = forms.DecimalField(validators=[DecimalValidator(4096,0)])
    address = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)

    # Removed validate_slug for address and description fields, max lenght = model's fields
    # validators=[validate_slug]
    # validators=[validate_slug]
    