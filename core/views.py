from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from .models import Usuario, Mascota, Adopcion
from .serializers import (
    UsuarioSerializer, 
    MascotaSerializer, 
    AdopcionSerializer,
    MyTokenObtainPairSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "user": serializer.data,
                "message": "Usuario registrado exitosamente"
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class MascotaPagination(PageNumberPagination):
    page_size = 5  # 5 mascotas por página para visualizar paginación fácilmente
    page_size_query_param = 'page_size'
    max_page_size = 100

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all().order_by('-fecha_creacion')
    serializer_class = MascotaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = MascotaPagination

    def perform_create(self, serializer):
        # Asignar automáticamente el publicador al usuario actual
        serializer.save(publicador=self.request.user)

    def get_queryset(self):
        queryset = Mascota.objects.all().order_by('-fecha_creacion')
        
        # Filtrar por el publicador actual si se solicita ?mis_publicaciones=true
        mis_publicaciones = self.request.query_params.get('mis_publicaciones', None)
        if mis_publicaciones == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(publicador=self.request.user)
            
        # Filtros de búsqueda adicionales
        especie = self.request.query_params.get('especie', None)
        if especie:
            especies_list = especie.split(',')
            query_filter = Q()
            for esp in especies_list:
                esp_clean = esp.strip().lower()
                if esp_clean in ['dogs', 'perro', 'perros']:
                    query_filter |= Q(especie__icontains='perro')
                elif esp_clean in ['cats', 'gato', 'gatos']:
                    query_filter |= Q(especie__icontains='gato')
                elif esp_clean in ['birds', 'ave', 'aves']:
                    query_filter |= Q(especie__icontains='ave')
                else:
                    query_filter |= Q(especie__icontains=esp_clean)
            queryset = queryset.filter(query_filter)

        nombre = self.request.query_params.get('nombre', None)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        tamano = self.request.query_params.get('tamano', None)
        if tamano:
            tam_clean = tamano.strip().lower()
            if tam_clean in ['small', 'pequeño', 'pequeno']:
                queryset = queryset.filter(tamano__icontains='peque')
            elif tam_clean in ['medium', 'mediano']:
                queryset = queryset.filter(tamano__icontains='median')
            elif tam_clean in ['large', 'grande']:
                queryset = queryset.filter(tamano__icontains='grand')
            else:
                queryset = queryset.filter(tamano__icontains=tamano)

        edad = self.request.query_params.get('edad', None)
        if edad:
            edad_clean = edad.strip().lower()
            if edad_clean == 'puppy':
                queryset = queryset.filter(
                    Q(edad__icontains='mes') | 
                    Q(edad__icontains='cachorro') | 
                    Q(edad__icontains='bebé')
                )
            elif edad_clean == 'young':
                queryset = queryset.filter(
                    Q(edad__icontains='joven') | 
                    Q(edad__icontains='1 año') | 
                    Q(edad__icontains='2 años')
                )
            elif edad_clean == 'adult':
                queryset = queryset.filter(
                    Q(edad__icontains='adulto') | 
                    Q(edad__icontains='3') | Q(edad__icontains='4') | 
                    Q(edad__icontains='5') | Q(edad__icontains='6') | 
                    Q(edad__icontains='7')
                )
            elif edad_clean == 'senior':
                queryset = queryset.filter(
                    Q(edad__icontains='mayor') | 
                    Q(edad__icontains='viejo') | 
                    Q(edad__icontains='8') | Q(edad__icontains='9') | 
                    Q(edad__icontains='10') | Q(edad__icontains='11') | Q(edad__icontains='12')
                )
            else:
                queryset = queryset.filter(edad__icontains=edad)

        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado__iexact=estado)

        return queryset

class AdopcionViewSet(viewsets.ModelViewSet):
    queryset = Adopcion.objects.all()
    serializer_class = AdopcionSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({'error': 'No se proporcionó ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = request.FILES['file']
        
        # Validar tipo de archivo
        if not file_obj.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            return Response({'error': 'Formato de imagen no válido'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Guardar archivo
        file_name = default_storage.save(f'pets/{file_obj.name}', ContentFile(file_obj.read()))
        file_url = default_storage.url(file_name)
        
        # Construir URI absoluta
        absolute_url = request.build_absolute_uri(file_url)
        
        return Response({'url': absolute_url}, status=status.HTTP_201_CREATED)


