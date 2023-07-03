from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from lms.models import *


def all_courses(request):
    return render(request, 'lms/all_courses.html')


def course_single(request, course_id):
    return render(request, 'lms/course_page_notenroll.html')


def my_courses(request):
    return HttpResponse('trash Список моих курсов')


def module_single(request, course_id, module_id):
    return HttpResponse('Курс номер: ' + str(course_id) + " модуль: " + str(module_id))


def assignments(request):
    user = request.user
    assignments = HomeworkAnswer.objects.filter(user=user)
    context = {
        'user': user,
        'assignments': assignments,
    }
    return render(request, 'lms/students_assignments.html', context=context)
