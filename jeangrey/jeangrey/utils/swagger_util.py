
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from jeangrey.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    test = serializers.CharField()
    class Meta:
        model = Service
        fields = '__all__'
