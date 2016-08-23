from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
# from django.template import loader

from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django import forms

from .forms import UserForm
from .models import Task

# Returns the list of tasks per user.
class IndexView(generic.ListView):
  template_name = 'todo/index.html'
  def get_queryset(self):
    if self.request.user.is_active == False:
      return []
    return self.request.user.task_set.all()

# Brings the user to the page with a the task name and the description
# of the task.
class DetailView(generic.DetailView):
  model = Task
  template_name = 'todo/detail.html'

# Uses the CreateView to create a Task object.
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

# Register and logs in a user.
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

# Logs in a user.
def login_user(request):
  logout(request)
  username=password=''
  if request.POST:
    username=request.POST['username']
    password=request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return redirect('index')
  return render(request, 'todo/login.html', {'username': username, 'password': password})

# Logs out a user.
def logout_user(request):
  logout(request)
  return redirect('register')
