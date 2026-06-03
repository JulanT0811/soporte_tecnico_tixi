from rest_framework import serializers
from soporte_tecnico.models import Category


class CategorySerializer(serializers.ModelSerializer):
    tickets_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'tickets_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_tickets_count(self, obj):
        return obj.tickets.count()
