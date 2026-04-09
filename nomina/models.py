from django.db import models
from negocios.models import Negocio

class Nomina(models.Model):
    id = models.BigAutoField(primary_key=True)
    empleado_nombre = models.TextField()
    cargo = models.TextField(blank=True, null=True)
    salario = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    mes = models.TextField(blank=True, null=True)
    fecha_pago = models.DateTimeField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nomina'

class NominaConcepto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nomina = models.ForeignKey(Nomina, models.DO_NOTHING)
    tipo = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    es_descuento = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nomina_conceptos'