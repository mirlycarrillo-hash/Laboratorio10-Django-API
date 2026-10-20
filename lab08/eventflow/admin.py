from django.contrib import admin
from .models import Espacio, RecursoTecnico


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'ubicacion_bloque',
        'aforo_maximo',
        'estado_operativo',
    )
    list_filter = ('estado_operativo', 'ubicacion_bloque')
    search_fields = ('nombre', 'ubicacion_bloque')


@admin.register(RecursoTecnico)
class RecursoTecnicoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_equipo',
        'codigo_inventario',
        'costo_alquiler',
        'cantidad_stock',
        'espacio',
    )
    list_filter = ('espacio',)
    search_fields = ('nombre_equipo', 'codigo_inventario')