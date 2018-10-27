from rest_framework import serializers
from .models import Task, SubTask


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'dueDate',
            'priority',
        )
        model = Task


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'dueDate',
            'priority',
            "isCompleted",
            "createdDate",
            "modifiedDate",
        )
        model = Task


class SubTaskCreateSerializer(serializers.ModelSerializer):

    task = TaskListSerializer(read_only=True)

    class Meta:
        fields = (
            'task',
            'id',
            'title',
            'description',
        )
        model = SubTask


class SubTaskListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'isCompleted',

            "createdDate",
            "modifiedDate",

        )
        model = SubTask
