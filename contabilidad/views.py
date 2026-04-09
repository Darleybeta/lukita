from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaccion, Factura
from .serializers import TransaccionSerializer, FacturaSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    serializer_class = TransaccionSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Transaccion.objects.filter(negocio_id=negocio_id)
        return Transaccion.objects.all()

class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Factura.objects.filter(negocio_id=negocio_id)
        return Factura.objects.all()