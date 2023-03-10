from django.http import HttpResponse
from django.shortcuts import render


def task_list(request):
    return HttpResponse('To Do List')