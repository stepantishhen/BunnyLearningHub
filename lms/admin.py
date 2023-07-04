from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_publish', 'time_create')
    list_display_links = ('name',)
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('name', 'description')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'social_link', 'avatar')
    list_display_links = ('user',)
    search_fields = ('user', 'description', 'social_link')


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'is_publish', 'time_create')
    list_display_links = ('name',)
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('name', 'description')


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('module', 'is_publish', 'deadline')
    list_display_links = ('module',)
    list_filter = ('is_publish', 'module')
    list_editable = ('is_publish',)
    search_fields = ('module',)


class HomeworkAnswerAdmin(admin.ModelAdmin):
    list_display = ('homework', 'user', 'time_create', 'time_update', 'mark', 'status')
    list_display_links = ('homework', 'user')
    list_filter = ('status', 'homework', 'user')
    list_editable = ('status', 'mark')
    search_fields = ('homework',)


class MessageCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'message', 'time_create', 'is_publish')
    list_display_links = ('message',)
    list_filter = ('user', 'course', 'is_publish')
    list_editable = ('is_publish',)
    search_fields = ('message',)


class MessageModuleAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'message', 'time_create', 'is_publish')
    list_display_links = ('message',)
    list_filter = ('user', 'module', 'is_publish')
    list_editable = ('is_publish',)
    search_fields = ('message',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkAnswer, HomeworkAnswerAdmin)
admin.site.register(MessageCourse, MessageCourseAdmin)
admin.site.register(MessageModule, MessageModuleAdmin)