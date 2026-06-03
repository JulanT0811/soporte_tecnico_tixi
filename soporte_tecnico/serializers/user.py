from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    created_tickets_count = serializers.SerializerMethodField()
    assigned_tickets_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined',
            'created_tickets_count', 'assigned_tickets_count'
        ]
        read_only_fields = ['date_joined']

    def get_created_tickets_count(self, obj):
        return obj.created_tickets.count()

    def get_assigned_tickets_count(self, obj):
        return obj.assigned_tickets.count()
