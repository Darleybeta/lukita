from rest_framework.decorators import api_view
from rest_framework.response import Response
from contabilidad.models import Transaccion
from inventario.models import Producto
from django.db.models import Sum
import anthropic
import os

@api_view(['POST'])
def analizar(request):
    negocio_id = request.data.get('negocio_id')
    pregunta = request.data.get('pregunta')

    # Traer datos financieros
    transacciones = list(Transaccion.objects.filter(
        negocio_id=negocio_id
    ).values('tipo', 'categoria', 'monto', 'fecha').order_by('-fecha')[:100])

    ingresos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='ingreso'
    ).aggregate(total=Sum('monto'))['total'] or 0

    egresos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='egreso'
    ).aggregate(total=Sum('monto'))['total'] or 0

    productos_bajo_stock = list(Producto.objects.filter(
        negocio_id=negocio_id
    ).extra(where=["stock <= stock_minimo"]).values('nombre', 'stock', 'stock_minimo'))

    # Formatear datos para Claude
    contexto = f"""
    RESUMEN FINANCIERO DEL NEGOCIO:
    - Total ingresos: ${ingresos:,.0f}
    - Total egresos: ${egresos:,.0f}
    - Balance actual: ${ingresos - egresos:,.0f}

    ÚLTIMAS 100 TRANSACCIONES:
    {transacciones}

    PRODUCTOS CON BAJO STOCK:
    {productos_bajo_stock}
    """

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    respuesta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Eres un agente financiero experto para negocios colombianos.
            Analiza estos datos y responde en español de forma clara y sencilla.

            DATOS DEL NEGOCIO:
            {contexto}

            PREGUNTA DEL USUARIO:
            {pregunta}

            Responde de forma práctica y útil. Si hay proyecciones,
            basalas en los datos históricos disponibles.
            """
        }]
    )

    return Response({
        'respuesta': respuesta.content[0].text,
        'datos_usados': {
            'ingresos': ingresos,
            'egresos': egresos,
            'balance': ingresos - egresos,
            'productos_bajo_stock': len(productos_bajo_stock)
        }
    })