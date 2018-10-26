from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Task, SubTask
from .serializers import TaskCreateSerializer, TaskListSerializer, \
    SubTaskCreateSerializer, SubTaskListSerializer


@permission_classes([IsAuthenticated])
class HomePage(TemplateView):
    template_name = 'todoApp/todoApp_home.html'


@permission_classes([IsAuthenticated])
class TaskListView(APIView):

    def get(self, request):

        """ GET - lists all tasks of user """

        tasks = Task.objects.filter(user=request.user, isDeleted=False)
        tasks_serialized = TaskListSerializer(tasks, many=True).data
        return Response(tasks_serialized)

    def post(self, request):

        """ POST - create new task """

        response_dict = {}
        task_serializer = TaskCreateSerializer(data=request.data)
        if task_serializer.is_valid():
            task = task_serializer.save(user=request.user)
            response_dict["message"] = "OK"
            response_dict["id"] = task.id
            return Response(response_dict)
        response_dict["message"] = "FAIL"
        response_dict["errors"] = task_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class TaskDetailView(APIView):

    def get(self, request, task_id):

        """ GET - show a task by id """

        response_dict = {}
        task = Task.objects.filter(id=task_id, isDeleted=False).first()
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        task_serialized = TaskListSerializer(task).data
        return Response(task_serialized)

    def put(self, request, task_id):

        """ PUT - update a task """

        response_dict = {}
        task = Task.objects.filter(id=task_id, isDeleted=False).first()
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        request_dict = request.data
        if "isCompleted" in request_dict.keys() and len(request_dict.keys()) == 1:
            if request_dict["isCompleted"] == "TRUE":
                task.markComplete()
            else:
                task.markPending()
            task.save()
            response_dict["message"] = "OK"
            response_dict["task_completed"] = task.isCompleted
            return Response(response_dict)
        task_serializer = TaskCreateSerializer(instance=task, data=request_dict)
        if task_serializer.is_valid():
            task_serializer.save()
            response_dict["message"] = "OK"
            return Response(response_dict)
        response_dict["message"] = "FAIL"
        response_dict["errors"] = task_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):

        """ DELETE - soft delete a task """

        response_dict = {}
        task = Task.objects.filter(id=task_id, isDeleted=False).first()
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        task.softDelete()
        task.save()
        response_dict["message"] = "Task deleted"
        return Response(response_dict)


@permission_classes([IsAuthenticated])
class SubTaskListView(APIView):

    def get(self, request, task_id):

        """ GET - show subtasks of a task by id"""

        task = get_object_or_404(Task, id=task_id)
        subtasks = SubTask.objects.filter(task=task, isDeleted=False)
        subtasks_serialized = SubTaskListSerializer(subtasks, many=True).data
        return Response(subtasks_serialized)

    def post(self, request, task_id):

        """ POST - create a new subtask of a task """

        response_dict = {}
        task = get_object_or_404(Task, id=task_id)
        subtask_serializer = SubTaskCreateSerializer(data=request.data)
        if subtask_serializer.is_valid():
            subtask = subtask_serializer.save(task=task)
            response_dict["message"] = "OK"
            response_dict["id"] = subtask.id
            return Response(response_dict)
        response_dict["message"] = "FAIL"
        response_dict["errors"] = subtask_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)


class SubTaskDetailView(APIView):

    def get(self, request, task_id, subtask_id):

        """ GET - show subtask in detail """

        response_dict = {}
        task = get_object_or_404(Task, id=task_id)
        sub_task = SubTask.objects.filter(id=subtask_id, isDeleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        sub_task_serialized = SubTaskListSerializer(sub_task).data
        return Response(sub_task_serialized)

    def put(self, request, task_id, subtask_id):

        """ PUT - update a subtask """

        response_dict = {}
        sub_task = SubTask.objects.filter(task__id=task_id, id=subtask_id, isDeleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        request_dict = request.data
        if "isCompleted" in request_dict.keys() and len(request_dict.keys()) == 1:
            if request_dict["isCompleted"] == "TRUE":
                sub_task.markComplete()
            else:
                sub_task.markPending()
            sub_task.save()
            response_dict["message"] = "OK"
            response_dict["subtask_completed"] = sub_task.isCompleted
            return Response(response_dict)
        sub_task_serializer = SubTaskCreateSerializer(instance=sub_task, data=request_dict)
        if sub_task_serializer.is_valid():
            sub_task_serializer.save()
            response_dict["message"] = "OK"
            return Response(response_dict)
        response_dict["message"] = "FAIL"
        response_dict["errors"] = sub_task_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, subtask_id):

        """ DELETE - soft delete a subtask """

        response_dict = {}
        sub_task = SubTask.objects.filter(task__id=task_id, id=subtask_id, isDeleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        sub_task.softDelete()
        sub_task.save()
        response_dict["message"] = "SubTask deleted"
        return Response(response_dict)



