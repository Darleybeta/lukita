from django.db import models
from negocios.models import Negocio

class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    precio = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    stock = models.BigIntegerField(blank=True, null=True)
    stock_minimo = models.BigIntegerField(blank=True, null=True)
    fecha_caducidad = models.DateTimeField(blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'

class Venta(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente_nombre = models.TextField()
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey('autenticacion.Usuario', models.DO_NOTHING, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'

class VentaDetalle(models.Model):
    id = models.BigAutoField(primary_key=True)
    venta = models.ForeignKey(Venta, models.DO_NOTHING)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, blank=True, null=True)
    cantidad = models.BigIntegerField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas_detalle'