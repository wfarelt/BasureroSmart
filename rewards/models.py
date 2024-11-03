from typing import Iterable
from core.models import User
from django.utils.crypto import get_random_string
from django.db import models

# Modelo para registrar recompenzas
class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=1, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.points_required} puntos) - {self.status}"

# Modelo para registrar canje de recompensas
class RewardClaim(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    claim_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=12, unique=True, default=get_random_string(12))
    status = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Ejecutado', 'Ejecutado'), ('Anulado','Anulado')], default='Pendiente')

    def __str__(self):
        return f"{self.reward.name} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.status == 'Pendiente':
            self.user.total_points -= self.reward.points_required
            self.user.save()
        elif self.status == 'Anulado':
            self.user.total_points += self.reward.points_required
            self.user.save()
        super().save(*args, **kwargs)