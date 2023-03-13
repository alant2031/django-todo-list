from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import *


class TaskList(ListView):
    template_name = "task_list.html"
    model = Task
    context_object_name = "tasks"


class TaskDetail(DetailView):
    template_name = "task_detail.html"
    model = Task
    context_object_name = "task"
