from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Negocio, Solicitud
from .serializers import NegocioSerializer, SolicitudSerializer

class NegocioViewSet(viewsets.ModelViewSet):
    queryset = Negocio.objects.all()
    serializer_class = NegocioSerializer

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        negocio = self.get_object()
        negocio.estado = 'activo'
        negocio.save()
        return Response({'mensaje': 'Negocio aprobado'})

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        negocio = self.get_object()
        negocio.estado = 'rechazado'
        negocio.save()
        return Response({'mensaje': 'Negocio rechazado'})

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer