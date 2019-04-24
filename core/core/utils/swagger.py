'''Helper class for Swagger spec.
'''
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from django.contrib.auth.models import User

swagger_info = openapi.Info(
	title="ONSA - CORE REST API",
	default_version='v1',
	description="""
<strong>Interactive documentation that lets users try out endpoints while learning about the ONSA - Core Server REST API.</strong>

<h3><u>How to:</u></h3>

<p><em> Begin by providing valid credentials to the "Login" endpoint. In order to do this, click the "Try it out" button within the "Post / Login Method". Complete the "name" and "password" fields, click "execute" and look out for the "token" value in the "Responses" section.</em></p>

<p><em> Now you can use the provided token to authenticate and test each endpoint of the API. In order to dothis, click on "Authorize", complete the "value" field writing the word "Bearer " (trailing whitespace plus the value of the adquired token and click "Authorize". In order to execute the request, use the "Try it out" button inside each action. </em></p>
""", )


class DisconnectionsDictSerializer(serializers.Serializer):
    '''Dictionary'''
    dc_date = serializers.DateField(help_text="Disconnection date: dd/MM/YY hh:mm")
    duration = serializers.IntegerField(help_text="Expressed in minutes as integer.")

class StatusMonitoringSerializer(serializers.ModelSerializer):
   
    status = serializers.CharField(help_text="Status of the device.")
    service_id = serializers.CharField(help_text="Service identifier.")
    latency = serializers.DecimalField(help_text="Average ICMP response time.", max_digits=5,
	decimal_places=2)
    # List of dictionarys
    disconnections = DisconnectionsDictSerializer(many=True)
    
    class Meta:
        model = User
        fields = ('status', 'service_id', 'latency', 'disconnections')

class ListQuerySerializer(serializers.Serializer):
    ''' this are the Query params '''
    tech = serializers.MultipleChoiceField(help_text="Type of the device technology", required=True ,
    choices=('cm', 'fo', 'dsl'))

class TrafficStreamDictSerializer(serializers.Serializer):
    ''' Dictionary '''
    timespan = serializers.DateTimeField()
    bps = serializers.IntegerField(help_text="Bits per second as integer")
    
class TrafficSerializer(serializers.ModelSerializer):
    '''test list of'''
    downstream = TrafficStreamDictSerializer(many=True)
    
    upstream = TrafficStreamDictSerializer(many=True)
    
    class Meta:
        model = User
        fields = ('downstream', 'upstream')

