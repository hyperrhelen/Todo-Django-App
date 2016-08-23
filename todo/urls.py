from django.conf.urls import url
from . import views

urlpatterns = [
  # /todo/
  url(r'^$', views.IndexView.as_view(), name='index'),
  # /todo/{ID}
  url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  
  # /todo/register
  url(r'^register/$', views.UserFormView.as_view(), name='register'),

  # /todo/login
  url(r'^login/$', views.login_user, name='login'),

  url(r'^logout/$', views.logout_user, name='logout'),

  # /todo/task/add
  url(r'^task/add/$', views.TaskCreate.as_view(), name='add'),
  # /todo/task/{ID}/
  url(r'^task/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='update'),
  # /todo/task/{ID}/delete
  url(r'^task/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='delete'),

]