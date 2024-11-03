from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('api/', include('core.urls')),  # Incluir las rutas de la app core
    path('', include('rewards.urls')),  # Incluir las rutas de la app rewards
]  + static('/dataset/', document_root='dataset')
