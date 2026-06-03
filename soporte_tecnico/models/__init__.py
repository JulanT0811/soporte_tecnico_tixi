from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    """Categorías para clasificar tickets"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Priority(models.Model):
    """Niveles de prioridad para tickets"""
    LEVEL_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Crítica'),
    ]
    
    level = models.IntegerField(choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#808080')  # Color hex
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Priorities"
        ordering = ['-level']

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Tickets de soporte técnico"""
    STATUS_CHOICES = [
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('on_hold', 'En Espera'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
        ('cancelled', 'Cancelado'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tickets')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"


class Comment(models.Model):
    """Comentarios en los tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ticket_comments')
    content = models.TextField()
    is_internal = models.BooleanField(default=False)  # Solo visible para staff
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.ticket.title}"


class Attachment(models.Model):
    """Archivos adjuntos en tickets"""
    ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'zip']
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ticket_attachments')
    file = models.FileField(
        upload_to='tickets/attachments/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # en bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename
