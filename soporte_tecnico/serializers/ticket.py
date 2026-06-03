from rest_framework import serializers
from soporte_tecnico.models import Ticket, Comment, Attachment, Category, Priority
from django.contrib.auth.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'is_internal', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSimpleSerializer(read_only=True)
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'uploaded_by', 'file', 'filename', 'file_size', 'file_size_display', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'file_size', 'filename', 'uploaded_at']

    def get_file_size_display(self, obj):
        """Convierte bytes a formato legible"""
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"


class TicketListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'status', 'category', 'category_name', 'priority', 'priority_name',
            'created_by', 'created_by_username', 'assigned_to', 'assigned_to_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class TicketDetailSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(is_active=True))
    category_detail = serializers.SerializerMethodField()
    priority_detail = serializers.SerializerMethodField()
    created_by = UserSimpleSerializer(read_only=True)
    assigned_to = UserSimpleSerializer(read_only=True, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    attachments_count = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'category', 'category_detail',
            'priority', 'priority_detail', 'created_by', 'assigned_to',
            'created_at', 'updated_at', 'resolved_at',
            'comments', 'attachments', 'comments_count', 'attachments_count'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'resolved_at']

    def get_category_detail(self, obj):
        from soporte_tecnico.serializers.category import CategorySerializer
        return CategorySerializer(obj.category).data

    def get_priority_detail(self, obj):
        return PrioritySerializer(obj.priority).data

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_attachments_count(self, obj):
        return obj.attachments.count()



