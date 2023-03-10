from django.urls import path

from .views import *

urlpatterns = [
    path('', task_list, name='tasks')
]
