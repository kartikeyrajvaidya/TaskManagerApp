from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import datetime

# Create your models here.

# task model -  user_id, title, due_date


class TimeStampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTask(TimeStampedModel):

    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
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
    due_date = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
