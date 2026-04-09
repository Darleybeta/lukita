from django.db import models
from negocios.models import Negocio
from autenticacion.models import Usuario

class Transaccion(models.Model):
    id = models.BigAutoField(primary_key=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    tipo = models.TextField(blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacciones'

class Factura(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero_factura = models.TextField()
    cliente_nombre = models.TextField(blank=True, null=True)
    cliente_contacto = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facturas'