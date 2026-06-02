from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, MascotaViewSet, AdopcionViewSet, ImageUploadView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'adopciones', AdopcionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', ImageUploadView.as_view(), name='image_upload'),
]

