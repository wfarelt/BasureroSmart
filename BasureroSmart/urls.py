from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('api/', include('core.urls')),  # Incluir las rutas de la app core
    path('', include('rewards.urls')),  # Incluir las rutas de la app rewards
]

# Servir archivos estáticos y de medios solo en desarrollo
if settings.DEBUG:
    urlpatterns += static('/dataset/', document_root='dataset')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
