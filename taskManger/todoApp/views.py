from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .models import Task, SubTask
from .serializers import TaskCreateSerializer, TaskListSerializer, \
    SubTaskCreateSerializer, SubTaskListSerializer
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils.deprecation import MiddlewareMixin


class HomePage(LoginRequiredMixin,TemplateView):
    template_name = 'todoApp/todoApp_home.html'


@permission_classes([IsAuthenticated])
class TaskListView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskListView, self).dispatch(request, *args, **kwargs)



    def get(self, request):
        """ GET - lists all tasks of user """

        response_dict = {}

        filter_type = request.GET.get("filter", "")
        today = datetime.date.today()
        start_week =  today - datetime.timedelta(today.weekday())
        end_week = start_week + datetime.timedelta(6)
        start_nextweek =  end_week + datetime.timedelta(1)
        end_nextweek = start_nextweek + datetime.timedelta(6)
        print(filter_type)

        if filter_type == "All":
            tasks = Task.objects.filter(user=request.user, isDeleted=False)
        elif filter_type == "This Week":
            tasks = Task.objects.filter(user=request.user, isDeleted=False, dueDate__range=[start_week, end_week])
        elif filter_type == "Next Week":
            tasks = Task.objects.filter(user=request.user, isDeleted=False, dueDate__range=[start_nextweek, end_nextweek])
        elif filter_type == "Overdue":
            tasks = Task.objects.filter(user=request.user, isDeleted=False, isCompleted=False, dueDate__lt=today)
        else:
            tasks = Task.objects.filter(user=request.user, isDeleted=False, dueDate=today)


        if tasks is None:
            response_dict["message"] = "No Task For Today Enjoy"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)



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
        print(task)
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        task.softDelete()
        task.save()
        print("Done")
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
        print(subtask_serializer)
        if subtask_serializer.is_valid():
            print('Valid')
            subtask = subtask_serializer.save(task=task)
            response_dict["message"] = "OK"
            response_dict["id"] = subtask.id
            return Response(response_dict)
        print('NotValid')
        response_dict["message"] = "FAIL"
        response_dict["errors"] = subtask_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)


class SubTaskDetailView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SubTaskDetailView, self).dispatch(request, *args, **kwargs)

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

    @csrf_exempt
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


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
