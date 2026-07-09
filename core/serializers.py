from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario, Mascota, Foto, Adopcion

class UsuarioSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(source='telefono_wsp', required=False, allow_blank=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'tipo_rol', 'telefono', 'is_active', 'date_joined', 'datos_adicionales']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
            'date_joined': {'read_only': True}
        }

    def validate(self, attrs):
        if not attrs.get('username') and attrs.get('email'):
            attrs['username'] = attrs['email']
        return attrs

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ['id', 'url_imagen']

class MascotaSerializer(serializers.ModelSerializer):
    fotos = FotoSerializer(many=True, required=False)
    publicador_telefono = serializers.CharField(source='publicador.telefono_wsp', read_only=True)

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'edad', 'color', 'tamano', 'descripcion', 'estado', 'publicador', 'publicador_telefono', 'fotos']
        read_only_fields = ['publicador', 'publicador_telefono']

    def create(self, validated_data):
        fotos_data = validated_data.pop('fotos', [])
        mascota = Mascota.objects.create(**validated_data)
        for foto_data in fotos_data:
            Foto.objects.create(mascota=mascota, **foto_data)
        return mascota

    def update(self, instance, validated_data):
        fotos_data = validated_data.pop('fotos', None)
        
        # Actualizar campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar fotos si se proporcionaron
        if fotos_data is not None:
            # Eliminar fotos antiguas de la base de datos
            instance.fotos.all().delete()
            # Crear nuevas fotos
            for foto_data in fotos_data:
                Foto.objects.create(mascota=instance, **foto_data)
                
        return instance

class AdopcionSerializer(serializers.ModelSerializer):
    mascota_detalle = MascotaSerializer(source='mascota', read_only=True)
    adoptante_detalle = UsuarioSerializer(source='adoptante', read_only=True)

    class Meta:
        model = Adopcion
        fields = ['id', 'mascota', 'adoptante', 'fecha_adopcion', 'mascota_detalle', 'adoptante_detalle']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['tipo_rol'] = user.tipo_rol
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['tipo_rol'] = self.user.tipo_rol
        return data
