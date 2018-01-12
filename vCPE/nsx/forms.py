import json
from django import forms
from django.forms import ModelForm
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


    class Meta:
        model = PrivateIrsService
        fields = ('ip_segment','client')


