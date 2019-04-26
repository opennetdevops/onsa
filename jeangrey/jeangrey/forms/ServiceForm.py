from django import forms
from django.core.validators import validate_slug, validate_ipv46_address, DecimalValidator
from jeangrey.validators import validate_prefix

class ServiceForm(forms.Form):
    client = forms.CharField(max_length=50 )#, validators=[validate_slug])
    location = forms.CharField(max_length=50 )#, validators=[validate_slug])
    service_type = forms.CharField(max_length=50 )#, validators=[validate_slug])
    id = forms.CharField(max_length=50 )#, validators=[validate_slug])
    bandwidth = forms.DecimalField()#validators=[DecimalValidator(5,0)])
    client_network = forms.CharField(max_length=50, required=False) #, validators=[validate_ipv46_address])
    customer_location_id = forms.DecimalField()#validators=[DecimalValidator(10,0)])
    prefix = forms.DecimalField(required=False)#, validators=[validate_prefix])
    access_port_id = forms.DecimalField(required=False)#, validators=[DecimalValidator(10,0)])