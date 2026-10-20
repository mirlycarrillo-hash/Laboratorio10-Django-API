from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import EspacioViewSet, RecursoTecnicoViewSet

router = DefaultRouter()
router.register(r'espacios', EspacioViewSet)
router.register(r'recursos', RecursoTecnicoViewSet)

urlpatterns = [
    path('login/', obtain_auth_token),
    path('', include(router.urls)),
]