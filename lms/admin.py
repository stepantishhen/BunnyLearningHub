from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


class CourseAdmin(ModelAdmin):
    list_display = ('name', 'author', 'is_publish', 'time_create')
    list_display_links = ('name',)
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        # Restrict the queryset to only include courses where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(author=request.user.profile)


class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'description', 'social_link', 'avatar')
    list_display_links = ('user',)
    search_fields = ('user', 'description', 'social_link')


class ModuleAdmin(ModelAdmin):
    list_display = ('name', 'course', 'is_publish', 'time_create')
    list_display_links = ('name',)
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        # Restrict the queryset to only include modules of courses where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(course__author=request.user.profile)


class HomeworkAdmin(ModelAdmin):
    list_display = ('module', 'is_publish', 'deadline')
    list_display_links = ('module',)
    list_filter = ('is_publish', 'module')
    list_editable = ('is_publish',)
    search_fields = ('module',)

    def get_queryset(self, request):
        # Restrict the queryset to only include homework of modules where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(module__course__author=request.user.profile)


class HomeworkAnswerAdmin(ModelAdmin):
    list_display = ('homework', 'user', 'time_create', 'time_update', 'mark', 'status')
    list_display_links = ('homework', 'user')
    list_filter = ('status', 'homework', 'user')
    list_editable = ('status', 'mark')
    search_fields = ('homework',)

    def get_queryset(self, request):
        # Restrict the queryset to only include homework answers of users where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)


class MessageCourseAdmin(ModelAdmin):
    list_display = ('user', 'course', 'message', 'time_create', 'is_publish')
    list_display_links = ('message',)
    list_filter = ('user', 'course', 'is_publish')
    list_editable = ('is_publish',)
    search_fields = ('message',)

    def get_queryset(self, request):
        # Restrict the queryset to only include messages of courses where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(course__author=request.user.profile)


class MessageModuleAdmin(ModelAdmin):
    list_display = ('user', 'module', 'message', 'time_create', 'is_publish')
    list_display_links = ('message',)
    list_filter = ('user', 'module', 'is_publish')
    list_editable = ('is_publish',)
    search_fields = ('message',)

    def get_queryset(self, request):
        # Restrict the queryset to only include messages of modules where the author is the current user
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(module__course__author=request.user.profile)


admin.site.register(Course, CourseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkAnswer, HomeworkAnswerAdmin)
admin.site.register(MessageCourse, MessageCourseAdmin)
admin.site.register(MessageModule, MessageModuleAdmin)
