from rest_framework import serializers
from .models import Usuario, Mascota, Foto, Adopcion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'email', 'tipo_rol', 'telefono_wsp', 'datos_adicionales']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ['id', 'url_imagen']

class MascotaSerializer(serializers.ModelSerializer):
    fotos = FotoSerializer(many=True, read_only=True)
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'descripcion', 'estado', 'publicador', 'fotos']
        read_only_fields = ['publicador']

class AdopcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopcion
        fields = '__all__'
