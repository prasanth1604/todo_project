from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id: 
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
