from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    ESTADO_POR_APROBAR = "Por aprobar"
    ESTADO_APROBADO = "Aprobado"
    ESTADO_CERRADO = "Cerrado"
    ESTADO_NOESBUG = "No es bug"
    ESTADO_NOARREGLADO = "No arreglado"
    ESTADOS = (
        (ESTADO_POR_APROBAR, "Por aprobar"),
        (ESTADO_APROBADO, "Aprobado"),
        (ESTADO_CERRADO, "Cerrado"),
        (ESTADO_NOESBUG, "No es bug"),
        (ESTADO_NOARREGLADO, "No arreglado"),
    )

    asunto = models.TextField(null=False, blank=False, default=None)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=30,choices=ESTADOS, default=ESTADO_POR_APROBAR)
    creado_el = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    propietario = models.ForeignKey(User, related_name='user')
    gravedad = models.IntegerField()

    def __str__(self):
      return str(self.asunto) + str(self.gravedad)

    class Meta:
        ordering = ["creado_el"]
        verbose_name_plural = "Incidencias"
