from rest_framework import serializers
from .models import User, WasteContainer, WasteType, Transaction

# Serializer para el modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_points']

# Serializer para el modelo WasteContainer
class WasteContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteContainer
        fields = ['id', 'name', 'location']

# Serializer para el modelo WasteType
class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = ['id', 'name', 'bonus_points']

# Serializer para el modelo Transaction
class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Mostrar información del usuario
    waste_type = WasteTypeSerializer(read_only=True)  # Mostrar tipo de residuo
    container = WasteContainerSerializer(read_only=True)  # Mostrar contenedor

    # Campos para permitir que se ingresen IDs en la creación
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    waste_type_id = serializers.PrimaryKeyRelatedField(
        queryset=WasteType.objects.all(), source='waste_type', write_only=True
    )
    container_id = serializers.PrimaryKeyRelatedField(
        queryset=WasteContainer.objects.all(), source='container', write_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'user_id', 'waste_type', 'waste_type_id', 
            'container', 'container_id', 'date', 'points_awarded'
        ]
