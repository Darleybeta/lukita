from django.db import models

class Negocio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    nombre_dueño = models.TextField(blank=True, null=True)
    nit_cedula = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    correo = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    tipo_negocio = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'negocios'

class Solicitud(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_negocio = models.TextField()
    nombre_dueño = models.TextField(blank=True, null=True)
    nit_cedula = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    correo = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    tipo_negocio = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    motivo_rechazo = models.TextField(blank=True, null=True)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitudes'