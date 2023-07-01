from django.urls import path

from lms.views import *

urlpatterns = [
    path('', index),
]