from rest_framework.routers import DefaultRouter
from .views import WasteContainerViewSet, WasteTypeViewSet, TransactionViewSet
from django.urls import path
from .views import RegisterUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'containers', WasteContainerViewSet, basename='container')
router.register(r'waste-types', WasteTypeViewSet, basename='waste-type')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]