from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WasteContainer, WasteType, Transaction
from .serializers import (
    WasteContainerSerializer, WasteTypeSerializer, TransactionSerializer
)

# ViewSet para los contenedores de basura
class WasteContainerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WasteContainer.objects.all()
    serializer_class = WasteContainerSerializer

# ViewSet para los tipos de residuos
class WasteTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WasteType.objects.all()
    serializer_class = WasteTypeSerializer

# ViewSet para las transacciones de reciclaje
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            # Actualizar puntos del usuario
            transaction.user.total_points += transaction.points_awarded
            transaction.user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
