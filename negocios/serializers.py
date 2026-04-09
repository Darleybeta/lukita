from rest_framework import serializers
from .models import Negocio, Solicitud

class NegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocio
        fields = '__all__'

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'