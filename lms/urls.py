from django.urls import path

from lms.views import *

urlpatterns = [
    path('all_courses/', all_courses), # ../lms/all_couses/
    path('course/<int:course_id>', course_single),
    path('my_courses/', my_courses),
    path('course/<int:course_id>/module/<int:module_id>',  module_single, name='module_single'),
    path('assignments/',  assignments),
]