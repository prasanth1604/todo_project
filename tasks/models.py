from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("task_detail", args=[str(self.id)])
    
