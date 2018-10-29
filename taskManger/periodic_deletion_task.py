import os

os.environ['DJANGO_SETTINGS_MODULE'] =  'taskManger.settings'
import django
django.setup()

from todoApp.models import Task
import time
from django.utils import timezone

expiry_date = timezone.now() - timezone.timedelta(30)
# print(expiry_date)
tasks = Task.objects.filter(isDeleted=True, deletedAtDate__lt=expiry_date)
# print(len(tasks))
tasks.delete()


# task = Task.objects.all().first()
# print(task.createdDate)
# print(timezone.get_current_timezone())
# date = task.dueDate
# timu = timezone.datetime(day=date.day, month=date.month, year=date.year , tzinfo=timezone.get_current_timezone())
# print(timu)
# print(date.timetuple())
# unix_timestamp = int(time.mktime(date.timetuple()))
# print(unix_timestamp)