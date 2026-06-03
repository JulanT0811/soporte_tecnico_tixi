from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from soporte_tecnico.models import Category
from soporte_tecnico.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD para Categorías"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Activar/Desactivar una categoría"""
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        return Response(self.get_serializer(category).data)
