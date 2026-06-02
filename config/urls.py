# config/urls.py
from django.contrib import admin
from django.urls import path, include

from soporte_tecnico.views.health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('soporte_tecnico.urls')),
    path('health/', health_check),
]