from rest_framework import serializers
from .models import Producto, Venta, VentaDetalle

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = '__all__'