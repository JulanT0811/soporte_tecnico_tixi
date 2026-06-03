from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.db.models import Q
from soporte_tecnico.models import Ticket, Comment, Attachment
from soporte_tecnico.serializers.ticket import (
    TicketListSerializer, TicketDetailSerializer, CommentSerializer, AttachmentSerializer
)
from soporte_tecnico.permissions import IsTicketOwnerOrAssigned


class TicketViewSet(viewsets.ModelViewSet):
    """CRUD para Tickets"""
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'priority', 'category', 'created_by', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Solo mostrar tickets del usuario o asignados a él (y staff ve todos)"""
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketListSerializer

    def perform_create(self, serializer):
        """Asignar el usuario actual como creador"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Asignar un ticket a un usuario"""
        ticket = self.get_object()
        user_id = request.data.get('user_id')
        
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
            ticket.assigned_to = user
            ticket.save()
            return Response(TicketDetailSerializer(ticket).data)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Cambiar estado de un ticket"""
        ticket = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in Ticket.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Estado inválido. Opciones: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = new_status
        if new_status == 'resolved':
            ticket.resolved_at = timezone.now()
        ticket.save()
        return Response(TicketDetailSerializer(ticket).data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Obtener estadísticas de un ticket"""
        ticket = self.get_object()
        return Response({
            'id': ticket.id,
            'title': ticket.title,
            'comments_count': ticket.comments.count(),
            'attachments_count': ticket.attachments.count(),
            'time_to_resolve': str(ticket.resolved_at - ticket.created_at) if ticket.resolved_at else None,
        })


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD para Comentarios"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Asignar el usuario actual como autor"""
        serializer.save(author=self.request.user)


class AttachmentViewSet(viewsets.ModelViewSet):
    """CRUD para Adjuntos"""
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']

    def perform_create(self, serializer):
        """Asignar el usuario actual como quien subió el archivo"""
        file_obj = self.request.FILES.get('file')
        serializer.save(
            uploaded_by=self.request.user,
            filename=file_obj.name,
            file_size=file_obj.size
        )

