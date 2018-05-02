import json
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import *
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2TagWidget,
    ModelSelect2Widget, Select2Widget
)

def getHubsAsTuple():
    return Hub.objects.all().values_list('name','name')

def getScoAsTuple():
    return Sco.objects.all().values_list('name','name')



class IrsServiceForm(ModelForm):

    hub = forms.ModelChoiceField(
        queryset=Hub.objects.all(),
        label="Hub",
        widget=ModelSelect2Widget(
            model=Hub,
            search_fields=['name__icontains'],

        )
    )

    sco = forms.ModelChoiceField(
        queryset=Sco.objects.all(),
        label="SCO",
        widget=ModelSelect2Widget(
            model=Sco,
            search_fields=['name__icontains'],
            dependent_fields={'hub': 'hub'},
            max_results=500,
        )
    )

    hub.widget.attrs['data-width'] = '14em'
    sco.widget.attrs['data-width'] = '14em'
    #username = forms.CharField()
    #password = forms.CharField(widget=PasswordInput())


    class Meta:
        model = PublicIrsService
        fields = ('public_network','client', 'product_identifier')
        labels = {
            'public_network': 'Network segment',
            'product_identifier' : 'ID'
        }


