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
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at_date = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at_date = timezone.now()
        self.save()

    def mark_complete(self):
        self.is_completed = True
        self.save()

    def mark_pending(self):
        self.is_completed = False
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
