from rest_framework.decorators import api_view
from rest_framework.response import Response
from contabilidad.models import Transaccion
from inventario.models import Producto
from django.db.models import Sum, F

@api_view(['GET'])
def resumen_financiero(request):
    negocio_id = request.query_params.get('negocio_id')

    if not negocio_id:
        return Response({'error': 'negocio_id es requerido'}, status=400)

    ingresos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='ingreso'
    ).aggregate(total=Sum('monto'))['total'] or 0

    egresos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='gasto'
    ).aggregate(total=Sum('monto'))['total'] or 0

    balance = ingresos - egresos

    return Response({
        'ingresos': ingresos,
        'egresos': egresos,
        'balance': balance
    })


@api_view(['GET'])
def productos_bajo_stock(request):
    negocio_id = request.query_params.get('negocio_id')

    if not negocio_id:
        return Response({'error': 'negocio_id es requerido'}, status=400)

    productos = Producto.objects.filter(
        negocio_id=negocio_id,
        stock__lte=F('stock_minimo')
    )

    return Response({
        'productos': list(productos.values())
    })


@api_view(['GET'])
def transacciones_por_categoria(request):
    negocio_id = request.query_params.get('negocio_id')

    if not negocio_id:
        return Response({'error': 'negocio_id es requerido'}, status=400)

    data = Transaccion.objects.filter(
        negocio_id=negocio_id
    ).values('categoria').annotate(total=Sum('monto'))

    return Response(list(data))