from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView

from .models import *


class AppLoginView(LoginView): 
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("tasks")
    

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("tasks")
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form=form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    template_name = "task_list.html"
    model = Task
    context_object_name = "tasks"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = "task_detail.html"
    model = Task
    context_object_name = "task"

class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = "task_form.html"
    model = Task
    fields = 'title', 'description', 'complete'
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form=form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = "task_form.html"
    model = Task
    fields = 'title', 'description', 'complete'
    success_url = reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    template_name = "task_confirm_delete.html"
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
