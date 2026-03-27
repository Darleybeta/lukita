from django.db import models

class Negocio(models.Model                                                                                                             ):
    nombre = models.TextField()
    nombre_dueño = models.TextField()
    nit_cedula = models.TextField()
    telefono = models.TextField()
    correo = models.TextField()
    ciudad = models.TextField()
    tipo_negocio = models.TextField()
    estado = models.TextField(default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'negocios'