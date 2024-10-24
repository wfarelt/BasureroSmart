from rest_framework.routers import DefaultRouter
from .views import WasteContainerViewSet, WasteTypeViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'containers', WasteContainerViewSet, basename='container')
router.register(r'waste-types', WasteTypeViewSet, basename='waste-type')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
