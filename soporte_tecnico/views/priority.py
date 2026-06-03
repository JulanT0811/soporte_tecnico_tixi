from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from soporte_tecnico.models import Priority
from soporte_tecnico.serializers.priority import PrioritySerializer


class PriorityViewSet(viewsets.ModelViewSet):
    """CRUD para Prioridades"""
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['level', 'name']
    ordering = ['-level']
    search_fields = ['name', 'description']
