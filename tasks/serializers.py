from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer ធ្វើការបំប្លែង Task model instance <-> JSON.
    - នៅពេល GET: បំប្លែង Python object ទៅ JSON
    - នៅពេល POST/PUT: validate JSON ដែលបញ្ចូលមក ហើយបំប្លែងទៅ Python object វិញ
    """

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'is_completed',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title មិនអាចទទេបានទេ (title cannot be blank).")
        return value
