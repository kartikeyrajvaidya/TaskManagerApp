from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Task,SubTask
from .serializers import TaskSerializer,SubTaskSerializer
from django.views.generic import (TemplateView)


class HomePage(TemplateView):
    template_name = 'todoApp/todoApp_home.html'

class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
