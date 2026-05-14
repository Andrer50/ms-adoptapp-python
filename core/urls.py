from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, MascotaViewSet, AdopcionViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'adopciones', AdopcionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
