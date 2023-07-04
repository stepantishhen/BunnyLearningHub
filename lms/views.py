from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lms.models import *


@login_required
def all_courses(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'lms/all_courses.html', context=context)


@login_required
def course_single(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        'course': course,
        'modules': Module.objects.filter(course=course)
    }

    return render(request, 'lms/course_page_notenroll.html', context=context)


@login_required
def my_courses(request):
    user = request.user
    enrolled_courses = user.enrolled_courses.all()
    homeworks_per_course = {}

    for course in enrolled_courses:
        homework_answers = HomeworkAnswer.objects.filter(user=user, homework__course=course, status='rat')
        count = homework_answers.count()

        modules_count = Module.objects.filter(course=course).count()

        if modules_count > 0:
            percent = (count / modules_count) * 100
        else:
            percent = 0
        homeworks_per_course[course] = percent

    context = {
        'homeworks_per_course': homeworks_per_course
    }

    return render(request,
                  'lms/my_courses.html',
                  context=context)


@login_required
def module_single(request, course_id, module_id):
    return HttpResponse('Курс номер: ' + str(course_id) + " модуль: " + str(module_id))


@login_required
def assignments(request):
    user = request.user
    assignments = HomeworkAnswer.objects.filter(user=user)
    context = {
        'user': user,
        'assignments': assignments,
    }
    return render(request, 'lms/students_assignments.html', context=context)


