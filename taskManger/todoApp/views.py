from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Task,SubTask
from .serializers import TaskSerializer,SubTaskSerializer


class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
