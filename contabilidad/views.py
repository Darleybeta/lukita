from time import timezone
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

    def perform_create(self, serializer):
        factura = serializer.save()
        if factura.estado == 'pagada':
            self._crear_transaccion_si_no_existe(factura)

    def perform_destroy(self, instance):
        Transaccion.objects.filter(
            categoria='factura',
            descripcion=f'Factura {instance.numero_factura} - {instance.cliente_nombre}',
            negocio_id=instance.negocio_id
        ).delete()
        instance.delete()

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        factura = self.get_object()
        if factura.estado != 'pagada':
            factura.estado = 'pagada'
            factura.save()
            self._crear_transaccion_si_no_existe(factura)
        return Response({'mensaje': 'Factura marcada como pagada'})

    def _crear_transaccion_si_no_existe(self, factura):
        existe = Transaccion.objects.filter(
            categoria='factura',
            descripcion=f'Factura {factura.numero_factura} - {factura.cliente_nombre}',
            negocio_id=factura.negocio_id
        ).exists()

        if not existe:
            Transaccion.objects.create(
                monto=factura.total,
                tipo='gasto',
                categoria='factura',
                descripcion=f'Factura {factura.numero_factura} - {factura.cliente_nombre}',
                negocio_id=factura.negocio_id,
                usuario_id=factura.usuario_id,
                fecha=timezone.now()
            )