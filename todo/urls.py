from django.conf.urls import url
from . import views

urlpatterns = [
  # /todo/
  url(r'^$', views.index, name='index'),
  # /todo/{ID}
  url(r'^(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
  # /todo/{ID}/favorite
  url(r'^done/$', views.done, name='done'),
]