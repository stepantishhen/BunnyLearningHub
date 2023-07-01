from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from lms.models import Module
def index(request):
    return render(request, 'lms/base.html')