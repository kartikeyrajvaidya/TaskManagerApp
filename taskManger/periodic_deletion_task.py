import os

os.environ['DJANGO_SETTINGS_MODULE'] =  'taskManger.settings'
import django
django.setup()

from todoApp.models import Task
import datetime
from django.utils import timezone

expiry_date = timezone.now() - timezone.timedelta(30)
# print(expiry_date)
tasks = Task.objects.filter(isDeleted=True, deletedAtDate__lt=expiry_date)
# print(len(tasks))
tasks.delete()
