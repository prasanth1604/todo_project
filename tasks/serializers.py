from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'updated_at', 'completed')
        read_only_fields = ('created_at', 'updated_at')

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S") if obj.created_at else None

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S") if obj.updated_at else None
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
