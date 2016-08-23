from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
# A task references the user.
# The list of tasks can be accessed by a user by doing: 
#   request.user.task_set.all()
class Task(models.Model):
  person = models.ForeignKey(User, on_delete=models.CASCADE)
  task_name = models.CharField(max_length=250)
  description = models.CharField(max_length=500)

  def get_absolute_url(self):
    return reverse('detail', kwargs={'pk': self.pk})

  def __str__(self):
    return self.task_name