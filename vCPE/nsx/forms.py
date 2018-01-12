import json
from django import forms
from django.forms import ModelForm
from .models import *










class IrsServiceForm(ModelForm):

    hub = ""
    sco = ""

    class Meta:
        model = PrivateIrsService
        fields = ('ip_segment','client')


    def __init__(self, *args, **kwargs):
        try:
            hub = kwargs['instance'].hub
        except KeyError:
            hub = 1 
        super(IrsServiceForm, self).__init__(*args, **kwargs)
        self.fields['sco'].queryset = Sco.objects.filter(hub=hub)