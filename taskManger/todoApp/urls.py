
from django.urls import path
from . import views

app_name = "todoApp"
urlpatterns = [
    path('',views.HomePage.as_view(),name='todoHome'),
    path('tasks/', views.TaskListView.as_view(), name="tasks"),
    path('tasks/<int:task_id>/', views.TaskDetailView.as_view(), name="tasks_detail"),
    path('tasks/<int:task_id>/subtasks/', views.SubTaskListView.as_view(), name="subtasks"),
    path('tasks/<int:task_id>/subtasks/<int:subtask_id>/', views.SubTaskDetailView.as_view(), name="subtasks_detail"),

]
