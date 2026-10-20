import django_filters
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Espacio, RecursoTecnico
from .serializers import EspacioSerializer, RecursoTecnicoSerializer


class RecursoFilter(django_filters.FilterSet):
    costo_min = django_filters.NumberFilter(field_name='costo_alquiler', lookup_expr='gte')
    costo_max = django_filters.NumberFilter(field_name='costo_alquiler', lookup_expr='lte')

    class Meta:
        model = RecursoTecnico
        fields = ['espacio', 'costo_min', 'costo_max']


class EspacioViewSet(viewsets.ModelViewSet):
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['estado_operativo', 'ubicacion_bloque']
    search_fields = ['nombre', 'ubicacion_bloque']

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'No se puede eliminar: el espacio tiene recursos asignados.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RecursoTecnicoViewSet(viewsets.ModelViewSet):
    queryset = RecursoTecnico.objects.select_related('espacio')
    serializer_class = RecursoTecnicoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RecursoFilter
    search_fields = ['nombre_equipo', 'codigo_inventario']