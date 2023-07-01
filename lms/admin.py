from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Message)
admin.site.register(UserCourse)
admin.site.register(Homework)
admin.site.register(HomeworkAnswer)
admin.site.register(Topic)