import re

from rest_framework import serializers
from .models import Espacio, RecursoTecnico


class EspacioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Espacio
        fields = '__all__'

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()

    def validate_ubicacion_bloque(self, value):
        if not value.strip():
            raise serializers.ValidationError('La ubicación no puede estar vacía.')
        return value.strip()

    def validate_aforo_maximo(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'El aforo máximo debe ser un número entero mayor a cero.'
            )
        return value


class RecursoTecnicoSerializer(serializers.ModelSerializer):
    espacio_detalle = EspacioSerializer(source='espacio', read_only=True)

    class Meta:
        model = RecursoTecnico
        fields = '__all__'

    def validate_costo_alquiler(self, value):
        if value <= 0:
            raise serializers.ValidationError('El costo debe ser mayor a cero.')
        return value

    def validate_cantidad_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'La cantidad en stock no puede ser negativa.'
            )
        return value

    def validate_codigo_inventario(self, value):
        value = value.strip().upper()
        if not re.match(r'^[A-Z0-9\-]{3,50}$', value):
            raise serializers.ValidationError(
                'Código inválido. Use letras, números y guiones (mínimo 3 caracteres).'
            )
        return value