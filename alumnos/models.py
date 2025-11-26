from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnos')
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
    email = models.EmailField(verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    dni = models.CharField(max_length=10, verbose_name='DNI', unique=True)
    carrera = models.CharField(max_length=100, verbose_name='Carrera')
    fecha_ingreso = models.DateField(verbose_name='Fecha de Ingreso')
    promedio = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Promedio', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} - {self.dni}"