from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
  person = models.ForeignKey(User, on_delete=models.CASCADE)
  task_name = models.CharField(max_length=250)
  description = models.CharField(max_length=500)
  is_done = models.BooleanField(default=False)
  def __str__(self):
    return self.task_name