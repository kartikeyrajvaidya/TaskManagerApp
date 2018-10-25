from django.urls import path

from . import views

app_name='todoApp'

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
]
