from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo extendido de usuario para añadir la bonificación total

class User(AbstractUser):
    total_points = models.PositiveIntegerField(default=0, verbose_name="Total de Puntos")
   
    def __str__(self):
        return f"{self.username} - Puntos: {self.total_points}"

# Modelo para representar los contenedores de basura
class WasteContainer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Contenedor")
    location = models.CharField(max_length=255, verbose_name="Ubicación del Contenedor")

    def __str__(self):
        return f"{self.name} - {self.location}"

# Modelo para representar los tipos de residuos
class WasteType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tipo de Residuo")
    bonus_points = models.PositiveIntegerField(verbose_name="Bonificación en Puntos")

    def __str__(self):
        return f"{self.name} - {self.bonus_points} Puntos"

# Modelo para registrar cada reciclaje realizado por los usuarios
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE, verbose_name="Tipo de Residuo")
    container = models.ForeignKey(WasteContainer, on_delete=models.CASCADE, verbose_name="Contenedor")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Transacción")
    points_awarded = models.PositiveIntegerField(verbose_name="Puntos Otorgados")

    def __str__(self):
        return f"Transacción - {self.user.username}: {self.points_awarded} puntos"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    # Método para guardar la transacción y actualizar los puntos del usuario, solo si la transacción es nueva
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.total_points += self.points_awarded
            self.user.save()
        super().save(*args, **kwargs)