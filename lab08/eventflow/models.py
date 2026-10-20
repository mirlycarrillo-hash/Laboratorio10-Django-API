from django.db import models


class Espacio(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    ubicacion_bloque = models.CharField(max_length=100)
    aforo_maximo = models.PositiveIntegerField()  
    estado_operativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion_bloque})"


class RecursoTecnico(models.Model):
    nombre_equipo = models.CharField(max_length=150)
    codigo_inventario = models.CharField(max_length=50, unique=True)
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.PositiveIntegerField()
    espacio = models.ForeignKey(
        Espacio, on_delete=models.PROTECT, related_name='recursos'
    )

    def __str__(self):
        return f"{self.nombre_equipo} - [{self.codigo_inventario}]"