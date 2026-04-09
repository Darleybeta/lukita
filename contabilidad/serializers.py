from rest_framework import serializers
from .models import Transaccion, Factura

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'