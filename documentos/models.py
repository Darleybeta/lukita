from django.db import models
from negocios.models import Negocio
from autenticacion.models import Usuario

class Documento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    tipo = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    descripcion_ia = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentos'

class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    nit_cedula = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    correo = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    productos_que_vende = models.TextField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedores'

class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    tipo = models.TextField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorias'

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    telefono = models.TextField(blank=True, null=True)
    correo = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'