from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import datetime


class TimeStampedModel(models.Model):

    createdDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTask(TimeStampedModel):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    isCompleted = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    deletedAtDate = models.DateTimeField(blank=True, null=True)

    def softDelete(self):
        self.isDeleted = True
        self.deletedAtDate = timezone.now()
        self.save()

    def markComplete(self):
        self.isCompleted = True
        self.save()

    def markPending(self):
        self.isCompleted = False
        self.save()

    class Meta:
        abstract = True


class Task(BaseTask):

    PRIORITY_CHOICES = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Urgent")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dueDate = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    alert_enabled = models.BooleanField(default=False)
    alert_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def enable_alert(self, alert_time):
        self.alert_enabled = True
        self.alert_time = alert_time
        self.save()

    class Meta:
        ordering = ['dueDate']


class SubTask(BaseTask):

    task = models.ForeignKey(Task,related_name='subTasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
