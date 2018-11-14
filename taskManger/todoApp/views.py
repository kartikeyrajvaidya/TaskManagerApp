from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
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
            tasks = Task.objects.filter(user=request.user, is_deleted=False)
        elif filter_type == "This Week":
            tasks = Task.objects.filter(user=request.user, is_deleted=False, dueDate__range=[start_week, end_week])
        elif filter_type == "Next Week":
            tasks = Task.objects.filter(user=request.user, is_deleted=False, dueDate__range=[start_nextweek, end_nextweek])
        elif filter_type == "Overdue":
            tasks = Task.objects.filter(user=request.user, is_deleted=False, is_completed=False, dueDate__lt=today)
        else:
            tasks = Task.objects.filter(user=request.user, is_deleted=False, dueDate=today)

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

    def get(self, request, task_id):

        """ GET - show a task by id """

        response_dict = {}
        task = Task.objects.filter(id=task_id, is_deleted=False).first()
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        task_serialized = TaskListSerializer(task).data
        return Response(task_serialized)


    def put(self, request, task_id):

        """ PUT - update a task """

        response_dict = {}
        task = Task.objects.filter(id=task_id, is_deleted=False).first()
        print(task)
        if task is None:
            response_dict["message"] = "task with given id not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        request_dict = request.data
        print(request_dict.keys())
        print(len(request_dict.keys()))
        if "isCompleted" in request_dict.keys() and len(request_dict.keys()) == 2:
            print('Inside')
            if request_dict["isCompleted"] == "TRUE":
                task.mark_complete()
            else:
                task.mark_pending()
            task.save()
            response_dict["message"] = "OK"
            response_dict["task_completed"] = task.is_completed
            return Response(response_dict)
        task_serializer = TaskCreateSerializer(instance=task, data=request_dict)
        if task_serializer.is_valid():
            print('Valid')
            task_serializer.save()
            response_dict["message"] = "OK"
            return Response(response_dict)
        print('Not Valid')
        response_dict["message"] = "FAIL"
        response_dict["errors"] = task_serializer.errors
        return Response(response_dict, status=HTTP_400_BAD_REQUEST)


    def delete(self, request, task_id):

        """ DELETE - soft delete a task """
        response_dict = {}
        task = Task.objects.filter(id=task_id, is_deleted=False).first()
        print(task)
        if task is None:
            response_dict["message"] = "OK"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        task.softDelete()
        task.save()
        print("Done")
        response_dict["message"] = "OK"
        return Response(response_dict)


@permission_classes([IsAuthenticated])
class SubTaskListView(APIView):

    def get(self, request, task_id):

        """ GET - show subtasks of a task by id"""

        task = get_object_or_404(Task, id=task_id)
        subtasks = SubTask.objects.filter(task=task, is_deleted=False)
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

    def get(self, request, task_id, subtask_id):

        """ GET - show subtask in detail """

        response_dict = {}
        task = get_object_or_404(Task, id=task_id)
        sub_task = SubTask.objects.filter(id=subtask_id, is_deleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        sub_task_serialized = SubTaskListSerializer(sub_task).data
        return Response(sub_task_serialized)


    def put(self, request, task_id, subtask_id):

        """ PUT - update a subtask """

        response_dict = {}
        sub_task = SubTask.objects.filter(task__id=task_id, id=subtask_id, is_deleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        request_dict = request.data
        if "isCompleted" in request_dict.keys() and len(request_dict.keys()) == 2:
            if request_dict["isCompleted"] == "TRUE":
                sub_task.mark_complete()
            else:
                sub_task.mark_pending()
            sub_task.save()
            response_dict["message"] = "OK"
            response_dict["subtask_completed"] = sub_task.is_completed
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
        sub_task = SubTask.objects.filter(task__id=task_id, id=subtask_id, is_deleted=False).first()
        if sub_task is None:
            response_dict["message"] = "sub task for given task not found"
            return Response(response_dict, status=HTTP_404_NOT_FOUND)
        sub_task.soft_delete()
        sub_task.save()
        response_dict["message"] = "SubTask deleted"
        return Response(response_dict)


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
def enable_alert_for_task_view(request, task_id):
    response_dict = {}
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        hours_before = request.data["hours_before"] if "hours_before" in request.data.keys() else None
        if hours_before is None:
            response_dict["message"] = "bad request"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)
        if not hours_before.isdigit():
            response_dict["message"] = "bad request, its not a number"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)
        hours_before = int(hours_before)
        day_before = task.dueDate - datetime.timedelta(1)
        alert_time = timezone.datetime(
            day=day_before.day, month=day_before.month, year=day_before.year,
            tzinfo=timezone.get_current_timezone(), hour=24-hours_before)
        task.enable_alert(alert_time)
    task_serialized = TaskListSerializer(task).data
    return Response(task_serialized)
