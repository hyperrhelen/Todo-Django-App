from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# from django.template import loader

from .models import Task
from django.contrib.auth.models import User

# Create your views here.
def index(request):
  all_tasks = Task.objects.all()
  # print(all_tasks)
  # template = loader.get_template('todo/index.html')
  context = {
    'all_tasks': all_tasks,
  }
  # html = '<h1>All tasks</h1>'
  # for task in all_tasks:
  #   url = '/task/' + str(task.id) + '/'
  #   html += "<a href="+url+">"+task.task_name+"</a><br>"
  return render(request, 'todo/index.html', context)
  # return HttpResponse(template.render(context,request))

def detail(request, task_id):
  task = get_object_or_404(Task, id=task_id)
  # try:
  #   task = Task.objects.get(id=task_id)
  # except Task.DoesNotExist:
  #   raise Http404("Task does not exist.")
  return render(request, 'todo/detail.html', {'task': task})
  # return HttpResponse("<h2>TODO detail page " + str(task_id)+" .</h2>")

def done(request):
  try:
    selected_task = Task.objects.get(pk=request.POST['task'])
  except (KeyError, Task.DoesNotExist):
    return render(request, 'todo/index.html', {
      'task': task, 
      'error_message': "Not valid task",
      })
  else:
    selected_task.is_done = True
    selected_task.save()
    return render(request, 'todo/index.html', {'all_tasks': Task.objects.all(),})