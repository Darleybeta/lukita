from rest_framework import serializers
from .models import Nomina, NominaConcepto

class NominaConceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NominaConcepto
        fields = '__all__'

class NominaSerializer(serializers.ModelSerializer):
    conceptos = NominaConceptoSerializer(many=True, read_only=True)
    class Meta:
        model = Nomina
        fields = '__all__'