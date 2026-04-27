from django.db import models
from negocios.models import Negocio

class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    correo = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    rol = models.TextField(blank=True, null=True)
    contrasena = models.TextField(blank=True, null=True)
    negocio = models.ForeignKey(Negocio, models.DO_NOTHING, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True