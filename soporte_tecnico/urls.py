# soporte_tecnico/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from soporte_tecnico.views.health import health_check

router = DefaultRouter()

urlpatterns = [
    path('health/', health_check),
    path('', include(router.urls)),
]