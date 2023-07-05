from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from lms.models import *


@login_required
def all_courses(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    context = {
        'courses': Course.objects.all(),
        'profile': profile
    }
    return render(request, 'lms/all_courses.html', context=context)


@login_required
def course_single(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    all_messages = MessageCourse.objects.filter(course=course_id)
    profile = Profile.objects.filter(user=user).first()
    context = {
        'course': course,
        'modules': Module.objects.filter(course=course),
        'all_messages': all_messages,
        'author_profile': course.author,
        'profile': profile
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

    profile = Profile.objects.filter(user=user).first()
    context = {
        'homeworks_per_course': homeworks_per_course,
        'profile': profile
    }

    return render(request,
                  'lms/my_courses.html',
                  context=context)


@login_required
def module_single(request, course_id, module_id):
    module = Module.objects.get(course=course_id, pk=module_id)
    assignment = Homework.objects.filter(module=module)
    profile = Profile.objects.filter(user=user).first()
    context = {
        'module': module,
        'assignment': assignment,
        'profile': profile
    }
    return render(request, 'lms/module_single.html', context=context)

@login_required
def assignments(request):
    user = request.user
    assignments = HomeworkAnswer.objects.filter(user=user)
    profile = Profile.objects.filter(user=user).first()
    context = {
        'user': user,
        'assignments': assignments,
        'profile': profile
    }
    return render(request, 'lms/students_assignments.html', context=context)


def add_to_course(request, course_id):
    current_user = request.user
    Course.objects.get(pk=course_id).users.add(current_user)
    profile = Profile.objects.filter(user=current_user).first()
    context = {
        'course_id': course_id,
        'profile': profile
    }
    return redirect('course_single', context)

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpass']

        user.first_name = first_name
        user.last_name = last_name

        user.email = email

        if password and password == confirm_password:
            user.set_password(password)

        user.save()
    profile = Profile.objects.filter(user=user).first()
    context = {
        'profile': profile
    }
    return render(request, 'lms/profile_edit.html', context=context)