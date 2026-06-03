from rest_framework import serializers
from soporte_tecnico.models import Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'level', 'name', 'description', 'color', 'created_at']
        read_only_fields = ['created_at']
