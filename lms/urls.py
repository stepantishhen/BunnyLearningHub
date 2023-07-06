from django.urls import path

from lms.views import *

urlpatterns = [
    path('all_courses/', all_courses, name='all_courses'), # ../lms/all_couses/
    path('course/<int:course_id>', course_single, name='course_single'),
    path('my_courses/', my_courses, name='my_courses'),
    path('course/<int:course_id>/module/<int:module_id>',  module_single, name='module_single'),
    path('assignments/',  assignments, name='assignments'),
    path('add_to_course/<int:course_id>/', add_to_course, name='add_to_course'),
    path('profile_edit/', profile_edit, name='profile_edit'),
    path('search_courses/', search_courses, name='search_courses')
]