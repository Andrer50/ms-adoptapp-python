from rest_framework import viewsets, permissions
from .models import Usuario, Mascota, Adopcion
from .serializers import UsuarioSerializer, MascotaSerializer, AdopcionSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser] # Solo admin puede ver todos los usuarios por defecto

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Asignar automáticamente el publicador al usuario actual
        serializer.save(publicador=self.request.user)

class AdopcionViewSet(viewsets.ModelViewSet):
    queryset = Adopcion.objects.all()
    serializer_class = AdopcionSerializer
    permission_classes = [permissions.IsAuthenticated]
