from rest_framework import serializers
from .models import Todo


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'isCompleted',
            'dueDate',
            'priority',
        )
        model = Task

class SubTaskSerializer(serializers.ModelSerializer):

    task = TaskSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'isCompleted',
        )
        model = SubTask
