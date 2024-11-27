from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import WasteContainer, WasteType, Transaction
from .serializers import (
    WasteContainerSerializer, WasteTypeSerializer, TransactionSerializer, UserBonusSerializer,\
    RewardSerializer, RewardClaimSerializer
)
from rest_framework.views import APIView
# Importa el modelo de usuario personalizado
from .models import User
from .serializers import UserSerializer
from rewards.models import Reward, RewardClaim


#Vista para registrar nuevos usuarios:
class RegisterUserView(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)  # Permitir subir archivos

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para los contenedores de basura
class WasteContainerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WasteContainer.objects.all()
    serializer_class = WasteContainerSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación


# ViewSet para los tipos de residuos
class WasteTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer

# ViewSet para las transacciones de reciclaje
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    
    # Filtra las transacciones por el usuario autenticado    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)  # Filtra por el usuario autenticado

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            # Actualizar puntos del usuario
            transaction.user.total_points += transaction.points_awarded
            transaction.user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Consultar las bonificaciones acumuladas de un usuario
class UserBonusView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserBonusSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Consultar los premios disponibles (Rewards)
class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    
    # Filtra los rewards con status=true
    def get_queryset(self):
        return Reward.objects.filter(status=True)  # Filtra por el status activo


# ViewSet para las solicitudes de premios
class RewardClaimViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardClaimSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    
    # Filtra las solicitudes por el usuario autenticado
    def get_queryset(self):
        user = self.request.user
        return RewardClaim.objects.filter(user=user)  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reward = serializer.validated_data['reward']
            user = request.user
            if user.total_points >= reward.points_required and reward.stock > 0:
                # Crear la solicitud
                reward.stock -= 1  # Disminuye el stock
                reward.save()
                reward_claim = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'No tienes suficientes puntos o el premio está agotado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)