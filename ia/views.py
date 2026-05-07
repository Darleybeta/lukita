from rest_framework.decorators import api_view
from rest_framework.response import Response
from contabilidad.models import Transaccion, Factura
from inventario.models import Producto, Venta
from django.db.models import Sum
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

@api_view(['POST'])
def analizar(request):
    negocio_id = request.data.get('negocio_id')
    pregunta = request.data.get('pregunta')

    # ── Datos financieros ──
    ingresos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='ingreso'
    ).aggregate(total=Sum('monto'))['total'] or 0

    gastos = Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='gasto'
    ).aggregate(total=Sum('monto'))['total'] or 0

    balance = ingresos - gastos

    # ── Últimas transacciones ──
    ultimas_transacciones = list(Transaccion.objects.filter(
        negocio_id=negocio_id
    ).values('tipo', 'categoria', 'monto', 'descripcion', 'fecha')
    .order_by('-fecha')[:20])

    # ── Productos ──
    total_productos = Producto.objects.filter(negocio_id=negocio_id).count()

    productos_bajo_stock = list(Producto.objects.filter(
        negocio_id=negocio_id
    ).extra(where=["stock <= stock_minimo"]).values('nombre', 'stock', 'stock_minimo'))

    # ── Facturas pendientes ──
    facturas_pendientes = Factura.objects.filter(
        negocio_id=negocio_id, estado='pendiente'
    ).count()

    facturas_monto_pendiente = Factura.objects.filter(
        negocio_id=negocio_id, estado='pendiente'
    ).aggregate(total=Sum('total'))['total'] or 0

    # ── Ventas ──
    total_ventas = Venta.objects.filter(negocio_id=negocio_id).count()
    monto_ventas = Venta.objects.filter(
        negocio_id=negocio_id
    ).aggregate(total=Sum('total'))['total'] or 0

    # ── Categorías de gasto ──
    gastos_por_categoria = list(Transaccion.objects.filter(
        negocio_id=negocio_id, tipo='gasto'
    ).values('categoria').annotate(total=Sum('monto')).order_by('-total'))

    contexto = f"""
RESUMEN FINANCIERO COMPLETO:
- Total ingresos: ${ingresos:,.0f} COP
- Total gastos: ${gastos:,.0f} COP
- Balance actual: ${balance:,.0f} COP
- Estado: {"POSITIVO ✅" if balance >= 0 else "NEGATIVO ⚠️"}

INVENTARIO:
- Total productos registrados: {total_productos}
- Productos con bajo stock: {len(productos_bajo_stock)}
{f"- Productos críticos: {', '.join([p['nombre'] for p in productos_bajo_stock])}" if productos_bajo_stock else "- Sin productos en estado crítico"}

VENTAS:
- Total ventas realizadas: {total_ventas}
- Monto total en ventas: ${monto_ventas:,.0f} COP

FACTURAS DE PROVEEDORES:
- Facturas pendientes de pago: {facturas_pendientes}
- Monto pendiente: ${facturas_monto_pendiente:,.0f} COP

GASTOS POR CATEGORÍA:
{chr(10).join([f"- {g['categoria']}: ${g['total']:,.0f} COP" for g in gastos_por_categoria]) if gastos_por_categoria else "- Sin datos de categorías"}

ÚLTIMAS 20 TRANSACCIONES:
{chr(10).join([f"- [{t['tipo'].upper()}] {t['categoria']} | ${t['monto']:,.0f} | {t['descripcion'] or 'Sin descripción'}" for t in ultimas_transacciones]) if ultimas_transacciones else "- Sin transacciones registradas"}
    """

    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres LukyIA, el asistente financiero inteligente del sistema Lukita, 
una plataforma contable para pequeñas y medianas empresas colombianas.

Tu rol es:
- Analizar datos financieros reales del negocio y dar insights concretos
- Detectar patrones, tendencias y alertas en los datos
- Dar recomendaciones accionables y específicas basadas en los números
- Explicar conceptos financieros en términos simples para empresarios no contables
- Alertar sobre situaciones de riesgo como balance negativo, stock bajo o facturas pendientes

Reglas de respuesta:
- Siempre responde en español colombiano, claro y profesional
- Usa los datos reales proporcionados para fundamentar tus respuestas
- Sé específico con los números — no des respuestas vagas
- Estructura tu respuesta con secciones claras usando emojis como íconos
- Si el balance es negativo, prioriza recomendaciones para mejorar liquidez
- Si hay productos en bajo stock, menciona el impacto en ventas
- Máximo 300 palabras por respuesta — sé conciso y directo"""
            },
            {
                "role": "user",
                "content": f"""Aquí están los datos actuales del negocio:

{contexto}

Pregunta del administrador: {pregunta}

Responde de forma práctica, específica y basada en los datos reales del negocio."""
            }
        ],
        max_tokens=500,
        temperature=0.5
    )

    return Response({
        'respuesta': respuesta.choices[0].message.content,
        'datos_usados': {
            'ingresos': float(ingresos),
            'gastos': float(gastos),
            'balance': float(balance),
            'productos_bajo_stock': len(productos_bajo_stock),
            'facturas_pendientes': facturas_pendientes,
            'total_ventas': total_ventas,
        }
    })