from rest_framework.routers import DefaultRouter
from .views import WasteContainerViewSet, WasteTypeViewSet, TransactionViewSet, UserBonusView,\
    RewardViewSet, RewardClaimViewSet
from django.urls import path
from .views import RegisterUserView, UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'containers', WasteContainerViewSet, basename='container')
router.register(r'waste-types', WasteTypeViewSet, basename='waste-type')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'rewards', RewardViewSet, basename='reward')
router.register(r'reward-claims', RewardClaimViewSet, basename='reward-claim')


urlpatterns = router.urls

urlpatterns += [
    path('user/', UserView.as_view(), name='user'),  # Perfil de usuario
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('user-bonuses/<int:id>/', UserBonusView.as_view(), name='user_bonus'),  # Ver bonificación
]