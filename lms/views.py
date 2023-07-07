from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group
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
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        user = request.user
        course = Course.objects.get(id=course_id)
        MessageCourse.objects.create(user=user, message=comment_text, course=course)
        return redirect('course_single', course_id)
    elif request.method == 'GET':
        user = request.user
        course = Course.objects.get(id=course_id)
        all_messages = MessageCourse.objects.filter(course=course_id)
        profile = Profile.objects.filter(user=user).first()

        context = {
            'course': course,
            'modules': Module.objects.filter(course=course),
            'all_messages': all_messages,
            'author_profile': course.author,
            'profile': profile,
            'Profile': Profile,
            'is_user_in_course': request.user in course.users.all()
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
    user = request.user
    module = Module.objects.get(course=course_id, pk=module_id)
    assignment = Homework.objects.filter(module=module).first()
    profile = Profile.objects.filter(user=user).first()
    homework_answer = HomeworkAnswer.objects.filter(user=user, homework=assignment).first()
    messages = MessageModule.objects.filter(module=module)

    if request.method == 'POST':
        if 'homework_form' in request.POST:
            google_drive_link = request.POST.get('google_drive_link')
            if google_drive_link:
                homework_answer.google_disk_url_folder = google_drive_link
                homework_answer.status = 's'
                homework_answer.save()
                return redirect('module_single', course_id=course_id, module_id=module_id)
        elif 'message_form' in request.POST:
            message = request.POST.get('message')
            if message:
                MessageModule.objects.create(user=user, message=message, module=module)
                return redirect('module_single', course_id=course_id, module_id=module_id)

    context = {
        'module': module,
        'assignment': assignment,
        'profile': profile,
        'homework_answer': homework_answer,
        'messages': messages
    }
    return render(request, 'lms/module_single.html', context=context)


@login_required
def assignments(request):
    user = request.user
    assignments = HomeworkAnswer.objects.filter(user=user)
    completed_courses = Course.objects.filter(module__homework__homeworkanswer__user=user,
                                              module__homework__homeworkanswer__status='rat').distinct()
    profile = Profile.objects.filter(user=user).first()
    if request.method == "POST":
        deadline = request.POST.get('deadline')
        status = request.POST.get('status')
        course = request.POST.get('course')

        if status:
            assignments = assignments.filter(status=status)
        if course:
            assignments = assignments.filter(homework__module__course_id=course)
        if deadline:
            if deadline == '-homework__deadline':
                assignments = assignments.order_by('-homework__deadline')
            else:
                assignments = assignments.order_by('homework__deadline')

    assignments = assignments.order_by('-time_update')

    context = {
        'user': user,
        'assignments': assignments,
        'completed_courses': completed_courses,
        'profile': profile,
    }

    return render(request, 'lms/students_assignments.html', context=context)


def add_to_course(request, course_id):
    current_user = request.user
    Course.objects.get(pk=course_id).users.add(current_user)
    return redirect('course_single', course_id)


@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
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

        if 'avatar-file' in request.FILES:
            avatar_file = request.FILES['avatar-file']
            profile.avatar = avatar_file
            profile.save()

        user.save()
        profile.save()

    context = {
        'profile': profile
    }
    return render(request, 'lms/profile_edit.html', context=context)

@login_required
def search_courses(request):
    search_text = request.GET.get('search_text', '').strip()

    courses = Course.objects.filter(name__icontains=search_text, is_publish=True)

    results = []
    for course in courses:
        result = {
            'name': course.name,
            'author': course.author.user.username,
            'picture': course.picture.url,
            'url': reverse('course_single', args=[course.id]),
        }
        results.append(result)

    return JsonResponse(results, safe=False)


def my_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_courses')
        else:
            return redirect('lms:login')
    else:
        return render(request, 'lms/login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        role = request.POST.get('role')
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = second_name
        if role:
            my_group = Group.objects.get(name=role)
            my_group.user_set.add(user)
        return redirect('login')
    return render(request, 'lms/signup.html')


def index(request):
    return render(request, 'lms/index.html')