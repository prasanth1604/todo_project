from django.db import models
from datetime import date

class Task(models.Model):
    """
    A Task has:
      - title (text)
      - description (optional text)
      - is_completed (bool)
      - date (a calendar date)
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    # every Task *must* have a date; default=date.today back-fills existing rows
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.date} – {self.title}"
