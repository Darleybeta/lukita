from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Nomina, NominaConcepto
from .serializers import NominaSerializer, NominaConceptoSerializer
from contabilidad.models import Transaccion

class NominaViewSet(viewsets.ModelViewSet):
    serializer_class = NominaSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Nomina.objects.filter(negocio_id=negocio_id)
        return Nomina.objects.all()

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        nomina = self.get_object()
        nomina.estado = 'pagado'
        nomina.save()
        Transaccion.objects.create(
        monto=nomina.salario,
        tipo='gasto',  # ← cambiar egreso por gasto
        categoria='nomina',
        descripcion=f'Pago nómina {nomina.empleado_nombre} - {nomina.mes}',
        negocio_id=nomina.negocio_id
)
        return Response({'mensaje': 'Nómina pagada exitosamente'})

class NominaConceptoViewSet(viewsets.ModelViewSet):
    serializer_class = NominaConceptoSerializer

    def get_queryset(self):
        nomina_id = self.request.query_params.get('nomina_id')
        if nomina_id:
            return NominaConcepto.objects.filter(nomina_id=nomina_id)
        return NominaConcepto.objects.all()