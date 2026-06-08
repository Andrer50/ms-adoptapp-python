from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('ALBERGUE', 'Albergue'),
        ('USER', 'Usuario Adoptante/Publicador'),
    )
    telefono_wsp = models.CharField(max_length=20, blank=True)
    tipo_rol = models.CharField(max_length=10, choices=ROLES, default='USER')
    # PostgreSQL JSONB nativo
    datos_adicionales = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.username} - {self.tipo_rol}"

class Mascota(models.Model):
    ESTADOS = (
        ('DISPONIBLE', 'Disponible'),
        ('ADOPTADO', 'Adoptado'),
    )
    publicador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    tamano = models.CharField(max_length=20, blank=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='DISPONIBLE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Foto(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fotos')
    url_imagen = models.URLField() # Aquí guardarás la URL de Cloudinary/S3/etc.

class Adopcion(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE)
    adoptante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_adopcion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.mascota.estado = 'ADOPTADO'
            self.mascota.save(update_fields=['estado'])

    def delete(self, *args, **kwargs):
        mascota = self.mascota
        super().delete(*args, **kwargs)
        mascota.estado = 'DISPONIBLE'
        mascota.save(update_fields=['estado'])

    class Meta:
        verbose_name_plural = "Adopciones"