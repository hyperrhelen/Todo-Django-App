from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
# from django.template import loader

from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django import forms

from .forms import UserForm
from .models import Task


class IndexView(generic.ListView):
  template_name = 'todo/index.html'
  def get_queryset(self):
    return self.request.user.task_set.all()
    # return Task.objects.get(person__id=self.request.user.id)
    # return Task.objects.all()
    # return Task.objects.get(person=self.request.user)

class DetailView(generic.DetailView):
  model = Task
  template_name = 'todo/detail.html'


class TaskCreate(CreateView):
  model = Task
  fields = ['task_name', 'description']

  def form_valid(self, form):
    task = form.save(commit=False)
    task.person = self.request.user
    return super(TaskCreate,self).form_valid(form)

class TaskUpdate(UpdateView):
  model = Task
  fields = ['task_name', 'description']

class TaskDelete(DeleteView):
  model = Task
  success_url = reverse_lazy('index')
  # fields = ['task_name', 'description']


class UserFormView(View):
  form_class = UserForm
  template_name = 'todo/registration_form.html'

  def get(self, request):
    form = self.form_class(None)

    return render(request, self.template_name, {'form': form})
  
  def post(self, request):
    form = self.form_class(request.POST)

    if form.is_valid():
      user = form.save(commit=False)
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user.set_password(password)
      user.save()

      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          login(request, user)
          return redirect('index')
    return render(request, self.template_name, {'form':form})


class UserFormLogin(View):
  form_class = UserForm
  template_name = 'todo/login.html'

  def get(self, request):
    form = self.form_class(None)
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          login(request, user)
          return rediret('index')
    return render(request, self.template_name, {'form':form})
# # Create your views here.
# def index(request):
#   all_tasks = Task.objects.all()
#   # print(all_tasks)
#   # template = loader.get_template('todo/index.html')
#   context = {
#     'all_tasks': all_tasks,
#   }
#   # html = '<h1>All tasks</h1>'
#   # for task in all_tasks:
#   #   url = '/task/' + str(task.id) + '/'
#   #   html += "<a href="+url+">"+task.task_name+"</a><br>"
#   return render(request, 'todo/index.html', context)
#   # return HttpResponse(template.render(context,request))

# def detail(request, task_id):
#   task = get_object_or_404(Task, id=task_id)
#   # try:
#   #   task = Task.objects.get(id=task_id)
#   # except Task.DoesNotExist:
#   #   raise Http404("Task does not exist.")
#   return render(request, 'todo/detail.html', {'task': task})
#   # return HttpResponse("<h2>TODO detail page " + str(task_id)+" .</h2>")

