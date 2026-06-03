from rest_framework.permissions import BasePermission
from soporte_tecnico.models import Ticket


class IsTicketOwnerOrAssigned(BasePermission):
    """
    Permite que solo el creador del ticket o el usuario asignado puedan verlo
    (excepto staff que puede verlo todo)
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.created_by == request.user or obj.assigned_to == request.user


class IsCommentAuthor(BasePermission):
    """Permite que solo el autor del comentario pueda editarlo/borrarlo"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.author == request.user


class IsAttachmentUploader(BasePermission):
    """Permite que solo quien subió el archivo pueda borrarlo"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.uploaded_by == request.user