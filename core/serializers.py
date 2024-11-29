from rest_framework import serializers
from .models import User, WasteContainer, WasteType, Transaction
from rewards.models import Reward, RewardClaim

# Serializer para el modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'image_perfil', 'total_points']  # Incluye los campos que necesitas
        extra_kwargs = {
            'password': {'write_only': True},  # Asegura que el password no se devuelva en la respuesta
            'total_points': {'read_only': True}  # Asegura que los puntos no se devuelvan en la respuesta
        }

    def create(self, validated_data):
        # Crea un usuario utilizando el método `create_user`
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            image_perfil=validated_data.get('image_perfil')
        )
        return user


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

class UserBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'total_points']
    
    
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'name' , 'description', 'points_required', 'stock', 'image', 'status']

class RewardClaimSerializer(serializers.ModelSerializer):
    user = UserBonusSerializer(read_only=True)
    reward = RewardSerializer(read_only=True)
    
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    reward_id = serializers.PrimaryKeyRelatedField(
        queryset=Reward.objects.all(), source='reward', write_only=True
    )
    
    class Meta:
        model = RewardClaim
        fields = ['user', 'user_id', 'reward', 'reward_id', 'claim_date', 'code', 'status']
        
    def create(self, validated_data):
        reward_claim = RewardClaim.objects.create(
            user=validated_data['user'],
            reward=validated_data['reward']
        )
        return reward_claim