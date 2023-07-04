from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
    all_messages = MessageCourse.objects.filter(course=course_id)
    context = {
        'course': course,
        'modules': Module.objects.filter(course=course),
        'all_messages': all_messages,
        'profile': Profile.objects.get(user=request.user),
        'is_user_in_course': request.user in course.users.all(),
    }

    return render(request, 'lms/course_page_notenroll.html', context=context)


@login_required
def my_courses(request):
    user = request.user
    enrolled_courses = user.enrolled_courses.all()
    homeworks_per_course = {}

    for course in enrolled_courses:
        modules = Module.objects.filter(course=course)
        homework_count = 0
        module_count = modules.count()

        for module in modules:
            module_homework_count = HomeworkAnswer.objects.filter(user=user, homework__module=module,
                                                                  status='rat').count()
            if module_homework_count > 0:
                homework_count += module_homework_count

        if module_count != 0:
            percent = (homework_count / module_count) * 100
        else:
            percent = 0
        homeworks_per_course[course] = int(percent)

    context = {
        'homeworks_per_course': homeworks_per_course
    }

    return render(request,
                  'lms/my_courses.html',
                  context=context)


@login_required
def module_single(request, course_id, module_id):
    module = Module.objects.get(course=course_id, pk=module_id)
    assignment = Homework.objects.filter(module=module)
    context = {
        'module': module,
        'assignment': assignment
    }
    return render(request, 'lms/module_single.html', context=context)

@login_required
def assignments(request):
    user = request.user
    assignments = HomeworkAnswer.objects.filter(user=user)
    context = {
        'user': user,
        'assignments': assignments,
    }
    return render(request, 'lms/students_assignments.html', context=context)


def add_to_course(request, course_id):
    current_user = request.user
    Course.objects.get(pk=course_id).users.add(current_user)
    return redirect('course_single', course_id=course_id)
