from datetime import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Producto, Venta, VentaDetalle
from .serializers import ProductoSerializer, VentaSerializer, VentaDetalleSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Producto.objects.filter(negocio_id=negocio_id)
        return Producto.objects.all()

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        negocio_id = request.query_params.get('negocio_id')
        productos = Producto.objects.filter(
            negocio_id=negocio_id
        ).extra(where=["stock <= stock_minimo"])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class VentaViewSet(viewsets.ModelViewSet):
    serializer_class = VentaSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Venta.objects.filter(negocio_id=negocio_id)
        return Venta.objects.all()

    def perform_create(self, serializer):
        venta = serializer.save()
        # Crear transaccion de ingreso automaticamente
        from contabilidad.models import Transaccion
        Transaccion.objects.create(
            monto=venta.total,
            tipo='ingreso',
            categoria='venta',
            descripcion=f'Venta a {venta.cliente_nombre}',
            negocio_id=venta.negocio_id,
            usuario_id=venta.usuario_id,
            fecha=timezone.now() 
        )

class VentaDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = VentaDetalleSerializer

    def get_queryset(self):
        venta_id = self.request.query_params.get('venta_id')
        if venta_id:
            return VentaDetalle.objects.filter(venta_id=venta_id)
        return VentaDetalle.objects.all()

    def perform_create(self, serializer):
        detalle = serializer.save()
        # Descontar stock automaticamente
        producto = detalle.producto
        producto.stock -= detalle.cantidad
        producto.save()