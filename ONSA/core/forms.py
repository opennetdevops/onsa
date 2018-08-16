import json
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import *
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2TagWidget,
    ModelSelect2Widget, Select2Widget
)

# def getHubsAsTuple():
#     return Hub.objects.all().values_list('name','name')

# def getScoAsTuple():
#     return Sco.objects.all().values_list('name','name')



class ServiceCpeRelationForm(ModelForm):

    cpe = forms.ModelChoiceField(
        queryset=Cpe.objects.all(),
        label="Cpe",
        widget=ModelSelect2Widget(
            model=Cpe,
            search_fields=['name__icontains'],

        )
    )

    cpe_port = forms.ModelChoiceField(
        queryset=CpePort.objects.all(),
        label="CPE_Port",
        widget=ModelSelect2Widget(
            model=CpePort,
            search_fields=['name__icontains'],
            dependent_fields={'cpe': 'cpe'},
            max_results=500,
        )
    )

    cpe.widget.attrs['data-width'] = '14em'
    cpe_port.widget.attrs['data-width'] = '14em'




    # class Meta:
    #     model = ServiceCpeRelations
    #     fields = ('client', 'product_identifier', 'public_network')
    #     labels = {
    #         'public_network' : 'Network',
    #         'product_identifier' : 'ID'
    #     }
