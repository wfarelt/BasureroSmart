from django import forms
from core.models import WasteContainer
from .models import Reward, RewardClaim

# Formulario para registrar recompenzas
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required', 'stock', 'image', 'status']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'points_required': 'Puntos requeridos',
            'stock': 'Stock',
            'image': 'Imagen',
            'status': 'Estado'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'points_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
# Formulario para registrar canje de recompensas
class RewardClaimForm(forms.ModelForm):
    class Meta:
        model = RewardClaim
        fields = ['reward', 'status']
        labels = {
            'reward': 'Recompensa',
            'status': 'Estado'
        }
        widgets = {
            'reward': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

# Formulario para registrar contenedores de basura
class WasteContainerForm(forms.ModelForm):
    class Meta:
        model = WasteContainer
        fields = ['name', 'location', 'capacity', 'status']
        labels = {
            'name': 'Nombre',
            'location': 'Ubicación',
            'capacity': 'Capacidad',
            'status': 'Estado'
        }        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }
