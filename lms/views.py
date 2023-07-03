from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HomeworkAnswer, Course

from django.views.generic import ListView

from lms.models import Module


def all_courses(request):
    return render(request, 'lms/all_courses.html')


def course_single(request, course_id):
    return render(request, 'lms/course_page_notenroll.html')

@login_required
def my_courses(request):
    user = request.user
    enrolled_courses = user.enrolled_courses.all()
    homeworks_per_course = {}

    for course in enrolled_courses:
        homework_answers = HomeworkAnswer.objects.filter(user=user, homework__course=course, status='rat')
        print(homework_answers)
        count = homework_answers.count()

        modules_count = Module.objects.filter(course=course).count()
        print(modules_count)

        if modules_count > 0:
            percent = (count / modules_count) * 100
        else:
            percent = 0
        homeworks_per_course[course] = percent
    print(homeworks_per_course)
    context = {
        'homeworks_per_course': homeworks_per_course
    }

    return render(request,
                  'lms/my_courses.html',
                  context=context)


def module_single(request, course_id, module_id):
    return HttpResponse('Курс номер: ' + str(course_id) + " модуль: " + str(module_id))


def assignments(request):
    return HttpResponse('Домашние задания пользователя')
